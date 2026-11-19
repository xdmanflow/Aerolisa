/**
 * Aerolisa: TypeScript Functions on the Ontology (Functions repository, TypeScript v1).
 *
 * - riskIfDelayed:           what-if shown in Workshop ("if we wait N more days...")
 * - fleetBandCounts:         RED / AMBER / GREEN counts for the fleet overview chart
 * - scheduleInspection:      backs the ScheduleInspection action (creates a WorkOrder)
 * - acknowledgeRecommendation, closeWorkOrder: the rest of the decision loop
 *
 * Object and property names below come from foundry/ontology/ontology.yaml (API names).
 * After creating the object types, import them in the repo's "Resource imports" panel,
 * then `@foundry/ontology-api` generates the types used here.
 */
import {
    Double,
    Edits,
    Function,
    Integer,
    LocalDate,
    OntologyEditFunction,
    TwoDimensionalAggregation,
    UserFacingError,
} from "@foundry/functions-api";
import { Engine, InspectionRecommendation, ObjectSet, Objects, WorkOrder } from "@foundry/ontology-api";

/** Piecewise-linear CDF through (P10, .1), (P50, .5), (P90, .9) with linear tails.
 *  Same formula as src/aerolisa/planner/risk.py::quantile_cdf (keep them identical). */
export function quantileCdf(x: number, p10: number, p50: number, p90: number): number {
    const eps = 1e-6;
    const q50 = Math.max(p50, p10 + eps);
    const q90 = Math.max(p90, q50 + eps);
    const xs = [p10 - (0.1 * (q50 - p10)) / 0.4, p10, q50, q90, q90 + (0.1 * (q90 - q50)) / 0.4];
    const ys = [0, 0.1, 0.5, 0.9, 1];
    if (x <= xs[0]) return 0;
    if (x >= xs[4]) return 1;
    for (let i = 0; i < 4; i++) {
        if (x <= xs[i + 1]) {
            return ys[i] + ((ys[i + 1] - ys[i]) * (x - xs[i])) / (xs[i + 1] - xs[i]);
        }
    }
    return 1;
}

export class AerolisaFunctions {
    /** Probability that the engine's remaining life runs out before the (delayed) check. */
    @Function()
    public riskIfDelayed(rec: InspectionRecommendation, delayDays: Integer): Double {
        const cpd = Math.max(rec.cyclesPerDay ?? 0.1, 0.1);
        const cycles = ((rec.daysToNextCheck ?? 0) + delayDays) * cpd;
        return quantileCdf(cycles, rec.rulP10 ?? 0, rec.rulP50 ?? 0, rec.rulP90 ?? 0);
    }

    /** Engines per band, for a Workshop chart (bar / pie) on the fleet overview page. */
    @Function()
    public async fleetBandCounts(engines: ObjectSet<Engine>): Promise<TwoDimensionalAggregation<string>> {
        return engines.groupBy(e => e.band.topValues()).count();
    }

    /** Backs the ScheduleInspection action. Submission criteria configured in the action:
     *  plannedDate is today or later; status is OPEN or ACKNOWLEDGED. */
    @Edits(WorkOrder, InspectionRecommendation)
    @OntologyEditFunction()
    public scheduleInspection(
        rec: InspectionRecommendation,
        plannedDate: LocalDate,
        workType: string,
        createdBy: string,
        comment?: string,
    ): void {
        if ((rec.rank ?? 999) > 10 && (!comment || comment.trim().length < 10)) {
            throw new UserFacingError("This engine is not in the top 10: explain why it is inspected now (10+ characters).");
        }
        if (rec.status === "SCHEDULED") {
            throw new UserFacingError("An inspection is already scheduled for this recommendation.");
        }
        const now = new Date().toISOString();
        const id = `WO-${rec.engineId}-${now.replace(/[-:.TZ]/g, "").slice(0, 14)}`;
        const wo = Objects.create().workOrder(id);
        wo.engineId = rec.engineId;
        wo.recommendationId = rec.recommendationId;
        wo.workType = workType; // e.g. "BORESCOPE", "ENGINE_REMOVAL", "TREND_REVIEW"
        wo.plannedDate = plannedDate.toString();
        wo.status = "PLANNED";
        wo.comment = comment ?? "";
        wo.createdBy = createdBy;
        wo.createdAt = now;
        rec.status = "SCHEDULED";
    }

    @Edits(InspectionRecommendation)
    @OntologyEditFunction()
    public acknowledgeRecommendation(rec: InspectionRecommendation, comment: string): void {
        if (!comment || comment.trim().length < 5) {
            throw new UserFacingError("A comment is required to acknowledge without scheduling.");
        }
        rec.status = "ACKNOWLEDGED";
    }

    /** Closing finding = ground truth for the next model version (feedback loop). */
    @Edits(WorkOrder)
    @OntologyEditFunction()
    public closeWorkOrder(wo: WorkOrder, finding: string): void {
        const allowed = ["DEGRADATION_CONFIRMED", "NO_FINDING", "OTHER_DEFECT"];
        if (allowed.indexOf(finding) < 0) {
            throw new UserFacingError(`finding must be one of ${allowed.join(", ")}`);
        }
        wo.status = "CLOSED";
        wo.finding = finding;
        wo.closedAt = new Date().toISOString();
    }
}
