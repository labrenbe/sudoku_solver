<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <Sudoku/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Sudoku from '@/components/Sudoku.vue'; // @ is an alias to /src

@Component({
  components: {
    Sudoku,
  },
})
export default class Home extends Vue {}
</script>
