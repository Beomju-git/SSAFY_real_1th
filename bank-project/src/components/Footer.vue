<template>
  <footer class="footer">
    <p>© 2024 JuukJuuk Bank. All rights reserved.</p>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  text-align: center;
  padding: 20px;
  background-color: #f1f1f1;
  position: fixed;
  width: 100%;
  bottom: 0;
  left: 0;
  right: 0;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

@media (max-width: 600px) {
  .footer {
    padding: 15px;
    font-size: 14px;
  }
}

@media (min-width: 601px) and (max-width: 900px) {
  .footer {
    padding: 18px;
    font-size: 16px;
  }
}

@media (min-width: 901px) {
  .footer {
    padding: 20px;
    font-size: 18px;
  }
}
</style>
