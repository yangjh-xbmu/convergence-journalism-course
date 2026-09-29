<template>
  <footer class="lesson-footer">
    <span
      >融合新闻产品策划与制作 ·
      {{ $slidev.configs.lessonLabel || $slidev.configs.title }}</span
    >
    <span>{{ $slidev.nav.currentPage }} / {{ $slidev.nav.total }}</span>
  </footer>
</template>
