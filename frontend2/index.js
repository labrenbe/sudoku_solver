import axios from 'axios';

const sampleMatrix = [
    [[null, 1], [null, 1], [null, 1], [null, 2], [null, 2], [null, 2], [null, 3], [null, 3], [null, 3]],
    [[null, 1], [null, 1], [null, 1], [null, 2], [null, 2], [null, 2], [null, 3], [null, 3], [null, 3]],
    [[null, 1], [null, 1], [null, 1], [null, 2], [null, 2], [null, 2], [null, 3], [null, 3], [null, 3]],
    [[null, 4], [null, 4], [null, 4], [null, 5], [null, 5], [null, 5], [null, 6], [null, 6], [null, 6]],
    [[null, 4], [null, 4], [null, 4], [null, 5], [null, 5], [null, 5], [null, 6], [null, 6], [null, 6]],
    [[null, 4], [null, 4], [null, 4], [null, 5], [null, 5], [null, 5], [null, 6], [null, 6], [null, 6]],
    [[null, 7], [null, 7], [null, 7], [null, 8], [null, 8], [null, 8], [null, 0], [null, 0], [null, 0]],
    [[null, 7], [null, 7], [null, 7], [null, 8], [null, 8], [null, 8], [null, 0], [null, 0], [null, 0]],
    [[null, 7], [null, 7], [null, 7], [null, 8], [null, 8], [null, 8], [null, 0], [null, 0], [null, 0]]]

Vue.component('sudoku-matrix', {
    data: function() {
        return {
            matrix: sampleMatrix.map(x => toObj(x)),
            blockMode: false,
            selectedBlock: 0,
        }
    },
    template: `
        <div>
            <div style="font-size:20px;padding:20px">Sudoku Solver</div>
            <div class="matrix">
                <div v-for="row in matrix">
                    <div v-for="cell in row" class="cell" v-bind:class="getClass(cell.block)" @click="changeBlock(cell)">
                            <input v-if="!blockMode" class="cell-input square" type="text" v-model="cell.value" 
                            v-bind:class="getClass(cell.block)" @change="validateCell(cell)"/>
                        <div v-if="blockMode" class="cell-input unselectable no-pointer" style="width:24px;height:22px">{{cell.value}}</div>
                    </div>
                </div>
            </div>
            <div class="container">
                <button class="button unselectable" v-on:click="solve()"><span>Solve!</span></button>
                <div style="width:5%"/>
                <button class="button unselectable" v-on:click="numbers()" v-bind:class="{'button-selected': !blockMode}"><span>Enter Numbers</span></button>
                <div style="width:5%"/>
                <button class="button unselectable" v-on:click="blocks()" v-bind:class="{'button-selected': blockMode}"><span>Change Blocks</span></button>
            </div>
                <div class="container">
                <div style="width: 60%"/>
                <span style="width:30%; padding: 6px" class="unselectable">Selected Block Color</span>
                <div class="selected-block" style="width:5%" v-bind:class="getClass(selectedBlock)" @click="incrementSelectedBlock()"/>
            </div>
        </div>`,
    methods: {
        getClass(int) {
            return 'block' + int.toString();
        },
        blocks() {
            this.blockMode = true;
        },
        numbers() {
            this.blockMode = false;
        },
        changeBlock(cell) {
            if (this.blockMode) {
                cell.block = this.selectedBlock;
            }
        },
        validateCell(cell) {
            if (!(cell.value < 10 && cell.value > 0 && !(isNaN(cell.value)))) {
                cell.value = null;
            }
        },
        solve() {
            console.log('Solve!');
            const path = 'http://localhost:5000/';
            axios.get(path)
                .then((res) => {
                  console.log = res.data;
                })
                .catch((error) => {
                  // eslint-disable-next-line
                  console.error(error);
                });
        },
        incrementSelectedBlock() {
            this.selectedBlock = (this.selectedBlock + 1) % 9;
        }
    }
});

const vm = new Vue({
    el: '#sudoku-app',
});

function toObj (array) {
    return array.map(x => new Object({value : x[0], block: x[1]}))
}

function toVal (object) {
    return object.map(x => [x.value, x.block])
}