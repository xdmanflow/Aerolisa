const fs = require('fs');
const h = require('./build_report.js');
const { Document, Packer, Paragraph, TextRun, AlignmentType, Header, Footer, PageNumber, HeadingLevel } = h;

const { cover, confidentiality, acknowledgments, abstractEN, resumeFR } = require('./main.js');
const { toc, tableOfIllustrations, introduction, section1 } = require('./part2.js');
const { section2 } = require('./part3.js');
const { section3 } = require('./part4.js');
const { section4 } = require('./part5.js');
const { section5 } = require('./part7.js');
const { section6, bibliography, glossary, appendices } = require('./part6.js');

const header = new Header({
  children: [new Paragraph({
    alignment: AlignmentType.RIGHT,
    children: [new TextRun({ text: 'SAA — Predictive Maintenance of Turbofan Engines', size: 16, color: '888888' })],
  })],
});

const footer = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: '888888' })],
  })],
});

// Font sizes follow the CESI writing guide (Section 10, "La mise en page"):
// body text Arial 12pt (size 24 half-points); titles Arial bold 18-20pt (size 36-40);
// sub-titles Arial bold 16pt (size 32).
const doc = new Document({
  features: { updateFields: true },
  styles: {
    default: {
      document: { run: { font: 'Arial', size: 24 } },
    },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Arial', size: 40, bold: true, color: '1F3864' }, paragraph: { spacing: { before: 300, after: 150 } } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Arial', size: 32, bold: true, color: '2C6E91' }, paragraph: { spacing: { before: 250, after: 120 } } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Arial', size: 26, bold: true, italics: true, color: '2C6E91' }, paragraph: { spacing: { before: 200, after: 100 } } },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4
          margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 },
        },
      },
      headers: { default: header },
      footers: { default: footer },
      children: [
        ...cover,
        ...confidentiality,
        ...acknowledgments,
        ...abstractEN,
        ...resumeFR,
        ...toc,
        ...tableOfIllustrations,
        ...introduction,
        ...section1,
        ...section2,
        ...section3,
        ...section4,
        ...section5,
        ...section6,
        ...bibliography,
        ...glossary,
        ...appendices,
      ],
    },
  ],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('/home/claude/saa/SAA_Report_Predictive_Maintenance.docx', buffer);
  console.log('Document written successfully.');
});
