import Cell from '@/matrix/cell';

export default class Matrix {
  cells = Array<Array<Cell>>();

  constructor() {
    this.cells = [
      Matrix.createEmptyRow(0, 1, 2),
      Matrix.createEmptyRow(0, 1, 2),
      Matrix.createEmptyRow(0, 1, 2),
      Matrix.createEmptyRow(3, 4, 5),
      Matrix.createEmptyRow(3, 4, 5),
      Matrix.createEmptyRow(3, 4, 5),
      Matrix.createEmptyRow(6, 7, 8),
      Matrix.createEmptyRow(6, 7, 8),
      Matrix.createEmptyRow(6, 7, 8)];
  }

  toArray() {
    return this.cells.map((row) => row.map((cell) => cell.toArray()));
  }

  fromArray(array: Array<Array<Array<number>>>) {
    this.cells = array.map((row) => row.map((cell) => new Cell(cell[0], cell[1])));
  }

  private static createEmptyRow(block1: number, block2: number, block3: number) {
    return [
      new Cell(block1), new Cell(block1), new Cell(block1),
      new Cell(block2), new Cell(block2), new Cell(block2),
      new Cell(block3), new Cell(block3), new Cell(block3)];
  }
}
