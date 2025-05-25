<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/navbar.vue' // Assuming navbar.vue is in src/components
import Footer from '@/components/footer.vue' // Assuming footer.vue is in src/components
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <main class="flex-grow pt-16">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>
