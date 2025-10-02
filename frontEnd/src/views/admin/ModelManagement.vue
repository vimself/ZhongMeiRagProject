<template>
  <div class="admin-page">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">模型管理</h1>
        <p class="page-subtitle">配置和管理AI模型参数</p>
      </div>
    </div>

    <div class="under-construction">
      <i class="icon-construction"></i>
      <h2>功能开发中</h2>
      <p>此功能正在开发中，敬请期待...</p>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.admin-page {
  padding: 32px 48px;
  max-width: 1800px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 88px;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #666666;
  margin: 0;
}

.under-construction {
  text-align: center;
  padding: 120px 40px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.icon-construction::before {
  content: '🚧';
  font-size: 80px;
  display: block;
  margin-bottom: 24px;
}

.under-construction h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.under-construction p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}
</style>


