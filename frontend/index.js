const sampleMatrix = [
    [{num : 11}, {num : 12}, {num : 13}, {num : 14}, {num : 15}, {num : 16}, {num : 17}, {num : 18}, {num : 19}],
    [{num : 21}, {num : 22}, {num : 23}, {num : 24}, {num : 25}, {num : 26}, {num : 27}, {num : 28}, {num : 29}],
    [{num : 31}, {num : 32}, {num : 33}, {num : 34}, {num : 35}, {num : 36}, {num : 37}, {num : 38}, {num : 39}],
    [{num : 41}, {num : 42}, {num : 43}, {num : 44}, {num : 45}, {num : 46}, {num : 47}, {num : 48}, {num : 49}]]

Vue.component('sudoku-matrix', {
    data: function() {
        return {
            matrix: sampleMatrix,
        }
    },
    template: `
        <div class="grid-sudoku">
            <div v-for="row in matrix" class="grid-row">
                <div v-for="cell in row" class="grid-cell">
                    <input type="text" v-bind:key="cell.num" v-model="cell.num" class="grid-cell-editor" />
                </div>
            </div>
        </div>`
});
var vm = new Vue({
    el: '#sudoku-app',

});