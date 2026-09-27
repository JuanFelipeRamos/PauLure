<script setup>
import NavbarComponent from './components/NavbarComponent.vue';

</script>

<template>
  <div id="app">
    <header>
      <NavbarComponent />
    </header>
  
    <main>
      <RouterView />
    </main>
  
    <footer></footer>
  </div>
</template>

<style scoped>

</style>
