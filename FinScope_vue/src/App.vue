<script setup>
import { RouterView } from 'vue-router'
import NavigationBar from '@/components/NavigationBar.vue' // Assuming NavigationBar.vue is in src/components
import Footer from '@/components/footer.vue' // Assuming footer.vue is in src/components
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-900">
    <NavigationBar />
    <main class="flex-grow pt-16">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>
