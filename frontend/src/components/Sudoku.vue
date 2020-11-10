<template>
  <div>
    <div class="headline">Sudoku Solver</div>
      <div class="matrix">
        <div v-for="row in matrix" v-bind:key="row">
          <div v-for="cell in row" v-bind:key="cell" v-bind:class="this.getClass(cell.block)"
               @click="changeBlock(cell)" class="cell">
            <label>
              <input v-if="!blockMode" class="cell-input-number" type="text" v-model="cell.value"
                     v-bind:class="this.getClass(cell.block)" @change="this.validateCell(cell)"/>
            </label>
            <div v-if="blockMode" class="cell-input-block unselectable no-pointer">
              {{cell.value}}
            </div>
          </div>
        </div>
    </div>
    <div class="container">
      <button class="button unselectable" v-on:click="solve()"><span>Solve!</span></button>
      <div style="width:5%"/>
      <button class="button unselectable" v-on:click="setBlockMode(false)"
              v-bind:class="{'button-selected': !blockMode}"><span>Enter Numbers</span></button>
      <div style="width:5%"/>
      <button class="button unselectable" v-on:click="setBlockMode(true)"
              v-bind:class="{'button-selected': blockMode}"><span>Change Blocks</span></button>
    </div>
      <div class="container">
      <div style="width: 60%"/>
      <span style="width:30%; padding: 6px" class="unselectable">Selected Block Color</span>
      <div class="selected-block" style="width:5%" v-bind:class="getClass(selectedBlock)"
           @click="incrementSelectedBlock()"/>
    </div>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';
import Matrix from '@/matrix/matrix';
import Cell from '@/matrix/cell';

@Component
export default class Sudoku extends Vue {
  matrix = new Matrix();

  blockMode = false;

  selectedBlock = 0;

  static getClass(int: number) {
    return `block${int.toString()}`;
  }

  setBlockMode(blockMode: boolean) {
    this.blockMode = blockMode;
  }

  changeBlock(cell: Cell) {
    if (this.blockMode) {
      cell.setBlock(this.selectedBlock);
    }
  }

  static validateCell(cell: Cell) {
    if (cell.value != null) {
      if (cell.value < 10 && cell.value > 0 && !(Number.isNaN(cell.value))) {
        cell.setNull();
      }
    }
  }

  static solve() {
    console.log('Solve!');
    const path = 'http://localhost:5000/';
    axios.get(path)
      .then((res: any) => {
        // eslint-disable-next-line
        console.log = res.data;
      })
      .catch((error: any) => {
      // eslint-disable-next-line
        console.error(error);
      });
  }

  incrementSelectedBlock() {
    this.selectedBlock = (this.selectedBlock + 1) % 9;
  }
}
</script>

<style scoped>
* {
    margin: 0;
    text-align: center;
    font-size: 12px;
    font-family: 'Dosis', sans-serif;
    font-weight: bold;
}

select:focus,
input:focus,
textarea:focus,
button:focus {
    outline: none;
}

body {
    display: grid;
    grid-template-rows: 150px 1fr;
    font-family: 'Dosis', sans-serif;
}

#sudoku-app {
    display: grid;
    grid-template-rows: auto 1fr;
    justify-items: center;
}

.matrix {
    display: table;
    background: white;
    border: 3px solid black;
}

.cell {
    display: table-cell;
    padding: 10px;
    border: 1px solid black;
}

.cell-input-number {
    border: none;
    font-family: 'Dosis', sans-serif;
    font-weight: bold;
    text-align: center;
    font-size: 18px;
    width: 20px;
    height: 20px;
}

.cell-input-block {
    border: none;
    font-family: 'Dosis', sans-serif;
    font-weight: bold;
    text-align: center;
    font-size: 18px;
    width: 22px;
    height: 24px;
}

.container {
    display: inline-flex;
    grid-template-rows: auto auto;
    padding-top: 25px;
    width: 100%;
}

.no-pointer {
    pointer-events:none;
}

.unselectable {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.button {
    display: inline-block;
    border: 2px solid black;
    background-color: whitesmoke;
    color: black;
    padding: 6px;
    width: 30%;
}

.button-selected {
    background-color: lightskyblue;
}
.selected-block {
    display: inline-block;
    border: 2px solid black;
    color: black;
    padding: 6px;
}

.headline {
  font-size: 20px;
  padding: 20px;
}

.block0 {
    background: orangered;
}
.block1 {
    background: lightgreen;
}
.block2 {
    background: yellow;
}
.block3 {
    background: saddlebrown;
}
.block4 {
    background: violet;
}
.block5 {
    background: orange;
}
.block6 {
    background: olive;
}
.block7 {
    background: cyan;
}
.block8 {
    background: cornflowerblue;
}
</style>
