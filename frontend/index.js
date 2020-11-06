const sampleMatrix = [
    [[11, 1], [12, 1], [13, 1], [14, 2], [15, 2], [16, 2], [17, 3], [18, 3], [19, 3]],
    [[11, 1], [12, 1], [13, 1], [14, 2], [15, 2], [16, 2], [17, 3], [18, 3], [19, 3]],
    [[11, 1], [12, 1], [13, 1], [14, 2], [15, 2], [16, 2], [17, 3], [18, 3], [19, 3]],
    [[11, 4], [12, 4], [13, 4], [14, 5], [15, 5], [16, 5], [17, 6], [18, 6], [19, 6]],
    [[11, 4], [12, 4], [13, 4], [14, 5], [15, 5], [16, 5], [17, 6], [18, 6], [19, 6]],
    [[11, 4], [12, 4], [13, 4], [14, 5], [15, 5], [16, 5], [17, 6], [18, 6], [19, 6]],
    [[11, 7], [12, 7], [13, 7], [14, 8], [15, 8], [16, 8], [17, 0], [18, 0], [19, 0]],
    [[11, 7], [12, 7], [13, 7], [14, 8], [15, 8], [16, 8], [17, 0], [18, 0], [19, 0]],
    [[11, 7], [12, 7], [13, 7], [14, 8], [15, 8], [16, 8], [17, 0], [18, 0], [19, 0]]]


Vue.component('sudoku-matrix', {
    data: function() {
        return {
            matrix: sampleMatrix.map(x => toObj(x)),
            blockMode: false,
        }
    },
    template: `
        <div>
            <div class="matrix">
                <div v-for="row in matrix" class="grid-row">
                    <div v-for="cell in row" class="cell" v-bind:class="getClass(cell.block)" @click="incrementBlock(cell)">
                        <input v-if="!blockMode" type="text" v-model="cell.value" v-bind:class="getClass(cell.block)" class="cell-input" @change="validateCell(cell)"/>
                        <div v-if="blockMode" class="cell-input unselectable no-pointer">{{cell.value}}</div>
                    </div>
                </div>
            </div>
            <div class="buttons-container">
                <button class="button unselectable" v-on:click="solve()"><span>Solve!</span></button>
                <div class="button-div"/>
                <button class="button unselectable" v-on:click="numbers()" v-bind:class="{'button-selected': !blockMode}"><span>Enter Numbers</span></button>
                <div class="button-div"/>
                <button class="button unselectable" v-on:click="blocks()" v-bind:class="{'button-selected': blockMode}"><span>Change Blocks</span></button>
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
        incrementBlock(cell) {
            if (this.blockMode) {
                cell.block = (cell.block + 1) % 9;
            }
        },
        validateCell(cell) {
            if (!(cell.value < 10 && cell.value > 0 && !(isNaN(cell.value)))) {
                cell.value = null;
            }
        },
        solve() {
            console.log('Solve!');
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