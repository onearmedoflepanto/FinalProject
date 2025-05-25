import { authFetch } from "./api.js";

document.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("sign_up-form")
  const followersList = document.getElementById("followers-list")
  const followingsList = document.getElementById("followings-list")

  try {
    const data = await authFetch('accounts', 'mypage')
    document.getElementById("username").value = data.username || ""
    document.getElementById("email").value = data.email || ""
    document.getElementById("nickname").value = data.nickname || ""

    if (Array.isArray(data.followings) && data.followings.length > 0) {
      followingsList.innerHTML = ""
      data.followings.forEach(async user => {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center"
        li.innerText = user.nickname

        const btn = document.createElement("button")
        btn.className = "btn btn-sm btn-danger"
        btn.innerText = "언팔로우"
        btn.onclick = async () => {
          try {
            await authFetch('accounts', 'follow', `${user.id}`, 'POST')
            alert('언팔로우 되었습니다.')
            li.appendChild(btn);
            followingsList.appendChild(li)
          }
          catch (err) {
            alert('서버 오류 발생. 다시 시도해 주십시오.')
            console.log('언팔로우 실패', err)
          }
        }
      })
    } else {
      followingsList.innerHTML = "<li class='list-group-item'>팔로잉한 유저가 없습니다.</li>"
    }
    if (Array.isArray(data.followers) && data.followers.length > 0) {
      followersList.innerHTML = ""
      data.followers.forEach(user => {
        const li = document.createElement("li")
        li.className = "list-group-item"
        li.innerText = user.nickname
        followersList.appendChild(li)
      })
    } else {
      followersList.innerHTML = "<li class='list-group-item'>아직 나를 팔로우한 유저가 없습니다.</li>"
    }
    form.addEventListener('submit', async (formEvent) => {
      formEvent.preventDefault()

      let password = document.getElementById("password").value.trim()
      let nickname = document.getElementById("nickname").value.trim()
      let email = document.getElementById("email").value.trim()

      const updated = {}
      if (password) updated.password = password
      if (nickname) updated.nickname = nickname
      if (email) updated.email = email

      try {
        authFetch('accounts', 'mypage', '', 'PUT', updated)
        alert('회원 정보 수정 완료!')
        window.location.reload()
      }
      catch (err) {
        alert('서버에 오류가 발생했습니다. 다시 시도해 주세요.')
        console.log('마이페이지 수정 실패', err)
      }
    })
  }
  catch (err) {
    alert('데이터 조회 실패')
    console.log('데이터 조회 실패', err)
  }
})
