<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">API测试页面</h1>

    <div class="space-y-4">
      <button
        @click="testLogin"
        class="bg-blue-500 text-white px-4 py-2 rounded"
      >
        测试登录
      </button>

      <button
        @click="testDepartments"
        class="bg-green-500 text-white px-4 py-2 rounded"
      >
        测试获取部门
      </button>

      <button
        @click="checkToken"
        class="bg-yellow-500 text-white px-4 py-2 rounded"
      >
        检查Token
      </button>
    </div>

    <div class="mt-8">
      <h2 class="text-xl font-bold mb-2">结果:</h2>
      <pre class="bg-gray-100 p-4 rounded overflow-auto">{{ result }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const result = ref("");

const testLogin = async () => {
  try {
    const response = await $fetch("/api/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: {
        username: "admin",
        password: "admin123",
      },
    });

    if (response && response.success && response.data && response.data.token) {
      localStorage.setItem("auth_token", response.data.token);
      localStorage.setItem("user_info", JSON.stringify(response.data.user));
    }

    result.value = JSON.stringify(response, null, 2);
  } catch (error) {
    result.value = `Error: ${error.message}`;
  }
};

const testDepartments = async () => {
  try {
    const token = localStorage.getItem("auth_token");

    const response = await $fetch("/api/departments/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Token ${token}` : "",
      },
    });

    result.value = JSON.stringify(response, null, 2);
  } catch (error) {
    result.value = `Error: ${error.message}\n${JSON.stringify(error, null, 2)}`;
  }
};

const checkToken = () => {
  const token = localStorage.getItem("auth_token");
  const userInfo = localStorage.getItem("user_info");

  result.value = `Token: ${token}\nUser Info: ${userInfo}`;
};
</script>
