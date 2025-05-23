import { authFetch } from "./api.js"
import { getCurrentUserId } from "./api.js";


document.addEventListener("DOMContentLoaded", async () => {
  const pathSegments = window.location.pathname.split("/").filter(Boolean)
  const name = decodeURIComponent(pathSegments[pathSegments.length - 1])
  const currentUser = getCurrentUserId()

  await getComments()

  // 댓글 작성
  const commentInput = document.getElementById("comment-input")
  const commentForm = document.getElementById("comment-form")
  commentForm.addEventListener("submit", async (event) => {
    event.preventDefault()
    const content = commentInput.value
    if (!content) {
      alert("댓글을 입력하세요!")
      return;
    }
    if (currentUser == null) {
      alert("로그인이 필요합니다.")
      location.href = "/login.html"
      return
    }

    await authFetch('boards', 'comments', `${name}`, 'POST')
    await getComments()
  })

  const commentList = document.getElementById("user-comments")
  commentList.addEventListener('click', async (event) => {
    const editId = event.target.dataset.edit
    const deleteId = event.target.dataset.delete
    const followId = event.target.dataset.follow

    if (followId) {
      if (currentUser == null) {
        alert('로그인 해 주세요.')
        location.href = "/login"
        return
      }
      try {
        const message = await authFetch('accounts', `follow`)
        alert(message)
      }
      catch (err) {
        console.log('댓글 작성 실패', err)
        alert('댓글 작성 실패')
      }
    }

    if (deleteId) {
      if (!confirm("댓글을 삭제하시겠습니까?")) return
      try {
        await authFetch('boards', 'comments', deleteId, 'DELETE')
      }
      catch (err) {
        console.log('댓글 삭제 실패', err)
        alert('댓글 삭제 실패')
      }
    }

    if (editId) {
      const li = event.target.closest("li")
      const original = li.querySelector("div").innerText
      const newContent = prompt("수정할 내용", original.split("\n")[1])
      if (newContent === null) return

      try {
        authFetch('boards', 'comments', editId, 'PUT', { content: newContent })
        await getComments()
      }
      catch {
        alert('수정 실패')
        return
      }
    }
  })
})

async function getComments() {
  const pathSegments = window.location.pathname.split("/").filter(Boolean)
  const name = decodeURIComponent(pathSegments[pathSegments.length - 1])
  try {
    const comments = await authFetch('boards', 'comments', `${name}`)

    commentList.innerHTML = "";

    if (Array.isArray(comments)) {
      comments.forEach((comment) => {
        const isOwner = comment.user_id === currentUser;
        const commentDisplay = document.createElement("li");
        commentDisplay.className = "list-group-item d-flex justify-content-between align-items-start";

        commentDisplay.innerHTML = `
          <div>
            <strong>${comment.user}</strong><br>${comment.content}
            <div class="text-muted small">${new Date(comment.created_at).toLocaleString()}</div>
          </div>
          ${isOwner ? `
            <div>
              <button class="btn btn-sm btn-outline-secondary me-1" data-edit="${comment.id}">수정</button>
              <button class="btn btn-sm btn-outline-danger" data-delete="${comment.id}">삭제</button>
            </div>
          ` :
            `<div>
              <button class="btn btn-sm btn-primary ms-1" data-follow="${comment.user_id}">팔로우</button>
            </div>
          `}
        `;
        commentList.appendChild(commentDisplay);
      });
    }
  }

  catch {
    commentList.innerHTML = "<p>댓글 로딩에 실패하였습니다.</p>";
  }
}
