import { nonAuthFetch } from "./api.js"

document.addEventListener("DOMContentLoaded", async (event) => {
  event.preventDefault()

  const username = document.getElementById("username").value.trim()
  const password = document.getElementById("password").value.trim()

  if (!username || !password) {
    alert("아이디와 비밀번호를 입력하세요.")
    return
  }

  try {
    const data = await nonAuthFetch('accounts', 'login', '', 'POST', { username, password })
    localStorage.setItem("access", data.access)
    localStorage.setItem("refresh", data.refresh)
    alert("로그인 성공!")
    window.location.href = "/mypage/"
  }
  catch (err) {
    alert('서버 오류입니다. 다시 시도해 주세요.')
    console.log('로그인 실패', err)
  }
})