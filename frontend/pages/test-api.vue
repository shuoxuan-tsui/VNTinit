<template>
  <!--
    设计思路:
    - 这是一个纯功能性的开发者工具页面，因此 UI 设计非常简约，注重实用性。
    - 使用简单的按钮来触发不同的 API 请求。
    - `<pre>` 标签用于格式化地显示 API 返回的 JSON 结果，`JSON.stringify(response, null, 2)` 会将其美化，便于阅读。
  -->
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
        测试获取部门 (需要Token)
      </button>

      <button
        @click="checkToken"
        class="bg-yellow-500 text-white px-4 py-2 rounded"
      >
        检查本地Token
      </button>
    </div>

    <div class="mt-8">
      <h2 class="text-xl font-bold mb-2">结果:</h2>
      <pre class="bg-gray-100 p-4 rounded overflow-auto">{{ result }}</pre>
    </div>
  </div>
</template>

<script setup>
/**
 * API 测试页面脚本
 *
 * 重要提示:
 * - 这是一个用于开发的辅助页面，不应该被打包到生产环境中。
 * - 它提供了一种快速验证后端接口连通性、请求/响应格式以及认证机制的方法。
 *
 * 设计思路:
 * - **关注点分离**: 每个函数负责测试一个特定的API端点。
 * - **状态管理**: 使用一个简单的 `ref` (`result`) 来存储并显示最新一次的请求结果。
 * - **手动Token管理**: 此页面直接操作 `localStorage` 来存取 `auth_token`。
 *   这与 `auth.ts` 中使用 `useCookie` 的方式不同，主要是为了方便进行更底层、更直接的测试。
 *   开发者可以手动清除或修改 `localStorage` 中的 token 来模拟不同的认证状态。
 */
import { ref } from "vue";

// 用于在页面上显示API请求结果的响应式变量
const result = ref("");

/**
 * 测试登录接口。
 * - 模拟用户使用 'admin'/'admin123' 凭据进行登录。
 * - 成功后，将返回的 token 和用户信息手动存入 `localStorage`。
 */
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

    // 登录成功后，手动将 token 存储到 localStorage，以便后续需要认证的接口使用
    if (response && response.success && response.data && response.data.token) {
      localStorage.setItem("auth_token", response.data.token);
      localStorage.setItem("user_info", JSON.stringify(response.data.user));
    }

    // 将完整的响应对象格式化后显示在页面上
    result.value = JSON.stringify(response, null, 2);
  } catch (error) {
    result.value = `Error: ${error.message}`;
  }
};

/**
 * 测试需要认证的接口（获取部门列表）。
 * - 从 `localStorage` 读取之前登录时存储的 token。
 * - 将 token 放入请求的 `Authorization` 头中。
 * - 如果没有 token，请求头中 `Authorization` 为空，预期后端会返回401或403错误。
 */
const testDepartments = async () => {
  try {
    const token = localStorage.getItem("auth_token");

    const response = await $fetch("/api/departments/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        // 在请求头中携带 Token，格式为 "Token <your-token>"
        Authorization: token ? `Token ${token}` : "",
      },
    });

    result.value = JSON.stringify(response, null, 2);
  } catch (error) {
    // 捕获错误并显示详细信息，方便调试
    result.value = `Error: ${error.message}\n${JSON.stringify(error, null, 2)}`;
  }
};

/**
 * 检查当前存储在 `localStorage` 中的认证信息。
 * - 这是一个简单的调试工具，用于快速确认 token 是否已正确存储。
 */
const checkToken = () => {
  const token = localStorage.getItem("auth_token");
  const userInfo = localStorage.getItem("user_info");

  result.value = `Token: ${token}\nUser Info: ${userInfo}`;
};
</script>
