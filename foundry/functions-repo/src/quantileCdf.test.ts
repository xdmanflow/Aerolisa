// Run with the repo's test runner (jest). Mirrors tests/test_planner_and_transforms.py.
import { quantileCdf } from "./index";

describe("quantileCdf", () => {
    it("hits the quantiles", () => {
        expect(quantileCdf(10, 10, 20, 40)).toBeCloseTo(0.1);
        expect(quantileCdf(20, 10, 20, 40)).toBeCloseTo(0.5);
        expect(quantileCdf(40, 10, 20, 40)).toBeCloseTo(0.9);
    });
    it("is monotone and bounded", () => {
        let prev = -1;
        for (let x = 0; x < 60; x++) {
            const v = quantileCdf(x, 10, 20, 40);
            expect(v).toBeGreaterThanOrEqual(prev);
            prev = v;
        }
        expect(quantileCdf(0, 10, 20, 40)).toBe(0);
        expect(quantileCdf(100, 10, 20, 40)).toBe(1);
    });
});
