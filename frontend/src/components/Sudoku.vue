<template>
  <div>
    <div class="sudoku">
      <div class="headline">Sudoku Solver</div>
      <div class="matrix" v-if="matrix !== undefined">
        <div v-for="(row, index) in matrix.cells" v-bind:key="`row-${index}`">
          <div v-for="cell in row.filter(c => c !== undefined)" v-bind:key="cell.block + getUUID()"
               v-bind:class="getClass(cell.block)" @click="changeBlock(cell)" class="cell">
            <label v-bind:class="{'unselect no-pointer': blockMode}">
              <input class="cell-input-number"
                     type="text" v-model="cell.value" v-bind:class="getClass(cell.block)"
                     @change="validateCell(cell)"/>
            </label>
          </div>
        </div>
      </div>
      <div>
        <div class="container">
          <button class="button" v-on:click="solve(matrix)"><span>Solve</span></button>
          <div style="width:5%"/>
          <button class="button" v-on:click="setBlockMode(false)"
                  v-bind:class="{'button-selected': !blockMode}"><span>Enter Numbers</span></button>
          <div style="width:5%"/>
          <button class="button" v-on:click="setBlockMode(true)"
                  v-bind:class="{'button-selected': blockMode}"><span>Change Blocks</span></button>
        </div>
      </div>
      <div>
        <div class="container">
          <button class="button" v-on:click="clear()"><span>Clear</span></button>
          <div style="width:5%"/>
          <button class="button" v-on:click="generate(matrix)"><span>Generate</span></button>
        </div>
      </div>
      <div>
        <div class="container">
          <div style="width: 60%"/>
          <span style="width:30%; padding: 6px" class="unselect">Selected Block Color</span>
          <div class="selected-block" style="width:5%" v-bind:class="getClass(selectedBlock)"
               @click="incrementSelectedBlock()"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';
import Matrix from '@/matrix/matrix';
import Cell from '@/matrix/cell';
import { v4 as uuidv4 } from 'uuid';

@Component
export default class Sudoku extends Vue {
  matrix = new Matrix();
  BASE_URL = "";

  blockMode = false;

  selectedBlock = 0;

  // eslint-disable-next-line
  getClass(int: number) {
    return `block${int.toString()}`;
  }

  // eslint-disable-next-line
  getUUID() {
    return uuidv4();
  }

  setBlockMode(blockMode: boolean) {
    this.blockMode = blockMode;
  }

  changeBlock(cell: Cell) {
    if (this.blockMode) {
      cell.setBlock(this.selectedBlock);
    }
  }

  // eslint-disable-next-line
  validateCell(cell: Cell) {
    if (cell.value != null) {
      if (!(cell.value in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        || cell.value.toString() === '0') {
        cell.setNull();
      }
    }
  }

  clear() {
    this.matrix = new Matrix();
  }



  // eslint-disable-next-line
  solve(matrix: Matrix) {
    const path = process.env.VUE_APP_SOLVE_URL;
    axios.post(path, JSON.stringify(matrix.toArray()),
      {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((res: any) => {
        console.log(res)
        matrix.fromArray(res.data);
      })
      .catch((error: any) => {
      // eslint-disable-next-line
        console.error(error);
      });
  }

  // eslint-disable-next-line
  generate(matrix: Matrix) {
    const path = process.env.VUE_APP_GENERATE_URL;
    axios.get(path)
      .then((res: any) => {
        matrix.fromArray(res.data);
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

.sudoku {
    display: inline-block;
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
    width: 24px;
    height: 22px;
}

.container {
    display: inline-flex;
    grid-template-rows: auto auto;
    padding-top: 10px;
    width: 100%;
}

.no-pointer {
    pointer-events:none;
}

.unselect {
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
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
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
