<template>
  <div class="chat-page">
    <div class="page-header">
      <h1 class="page-title">智能问答</h1>
      <p class="page-subtitle">基于知识库的智能问答系统</p>
    </div>
    
    <div class="coming-soon">
      <i class="icon-construction"></i>
      <h2>功能开发中</h2>
      <p>智能问答功能即将上线，敬请期待...</p>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.chat-page {
  padding: 32px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
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

.coming-soon {
  text-align: center;
  padding: 120px 20px;
}

.icon-construction::before {
  content: '🚧';
  font-size: 80px;
  display: block;
  margin-bottom: 24px;
}

.coming-soon h2 {
  font-size: 24px;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.coming-soon p {
  font-size: 16px;
  color: #666666;
  margin: 0;
}
</style>

