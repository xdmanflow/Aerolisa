const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, TableOfContents, PageBreak, PageNumber, Footer, Header,
  LevelFormat, convertInchesToTwip, VerticalAlign, PositionalTab,
  PositionalTabAlignment, PositionalTabLeader, TabStopType, TabStopPosition,
} = require('docx');

const YELLOW = 'F5D91A';
const DARKBLUE = '1F3864';
const GREY = '595959';

function H1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 400, after: 200 } });
}
function H2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 300, after: 150 } });
}
function H3(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 100 } });
}
function P(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, italics: !!opts.italics, bold: !!opts.bold })],
    spacing: { after: 180, line: 276 },
    alignment: opts.align || AlignmentType.LEFT,
  });
}
function Bullet(text) {
  return new Paragraph({
    children: [new TextRun(text)],
    bullet: { level: 0 },
    spacing: { after: 100, line: 276 },
  });
}
function Caption(text) {
  return new Paragraph({
    children: [new TextRun({ text, italics: true, size: 19, color: GREY })],
    spacing: { after: 300, before: 80 },
    alignment: AlignmentType.CENTER,
  });
}
function imgParagraph(path, width, height) {
  return new Paragraph({
    children: [new ImageRun({ type: 'png', data: fs.readFileSync(path), transformation: { width, height } })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 80 },
  });
}
function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.shade ? { type: ShadingType.CLEAR, fill: opts.shade } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      children: [new TextRun({ text, bold: !!opts.bold, size: 20 })],
      alignment: opts.align || AlignmentType.LEFT,
    })],
  });
}

module.exports = { H1, H2, H3, P, Bullet, Caption, imgParagraph, cell,
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, TableOfContents, PageBreak, PageNumber, Footer, Header,
  LevelFormat, convertInchesToTwip, VerticalAlign,
  YELLOW, DARKBLUE, GREY };
