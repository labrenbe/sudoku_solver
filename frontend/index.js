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