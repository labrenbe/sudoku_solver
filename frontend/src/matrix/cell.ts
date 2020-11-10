export default class Cell {
  block: number;

  value: number | null;

  constructor(block: number, value?: number) {
    this.block = block;
    this.value = value || null;
  }

  toArray() {
    return [this.value, this.block];
  }

  fromArray([block, value]: Array<number>) {
    this.block = block;
    this.value = value === 0 ? null : value;
  }

  setNull() {
    this.value = null;
  }

  setBlock(block: number) {
    this.block = block;
  }
}
