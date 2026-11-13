<script setup>
import NavbarComponent from './components/NavbarComponent.vue';

const excludedRoutes = ['loginadmin', 'homepaneladmin']

</script>

<template>
  <div id="app">
    <header>
      <NavbarComponent v-if="!excludedRoutes.includes($route.name)" />
    </header>
  
    <main>
      <RouterView />
    </main>
  
    <footer></footer>
  </div>
</template>

<style scoped>

</style>
