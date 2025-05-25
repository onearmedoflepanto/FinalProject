import { nonAuthFetch } from "./api.js"

document.addEventListener("DOMContentLoaded", async (event) => {
  const form = document.getElementById("login-form");
  form.addEventListener('submit', async (formEvent) => {
    const username = document.getElementById("username").value.trim()
    const password = document.getElementById("password").value.trim()
    const nickname = document.getElementById("nickname").value.trim()
    const email = document.getElementById("email").value.trim()

    if (!username || !password || !nickname || !email) {
      alert("입력란을 전부 채우세요.")
      return
    }

    try {
      const data = await nonAuthFetch('accounts', 'sign_up', '', 'POST')
      localStorage.setItem("access", data.access)
      localStorage.setItem("refresh", data.refresh)
      alert("회원가입 하셨습니다. 축하합니다!")
      window.location.href = "127.0.0.1:8000/mypage/"
    }
    catch (err) {
      if (err) {
        alert('서버 오류입니다. 다시 시도해 주세요.')
        console.log('회원가입 실패', err)
      }
      else {
        alert('서버 오류입니다. 다시 시도해 주세요.')
      }
    }
  })
})