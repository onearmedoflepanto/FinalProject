import { authFetch } from "./api.js"

document.addEventListener("DOMContentLoaded", async () => {
  const pathSegments = window.location.pathname.split("/").filter(Boolean)
  const name = decodeURIComponent(pathSegments[pathSegments.length - 1])
  const API_URL = "http://127.0.0.1:8001/"

  const container = document.getElementById("scraped-comments")
  const favoriteBtn = document.getElementById("favorite-btn")

  try {
    const data = await authFetch("stocks", `detail/${name}`)

    document.getElementById("stock-name").innerText = data.stock.이름
    document.getElementById("stock-code").innerText = data.stock.코드
    document.getElementById("stock-price").innerText = data.stock.가격
    document.getElementById("stock-change").innerText = data.stock.등락률
    document.getElementById("stock-chart").src = API_URL + data.stock.차트

    // 댓글 표시
    if (Array.isArray(data.comments)) {
      data.comments.forEach(comment => {
        const li = document.createElement("li")
        li.className = "list-group-item"
        li.innerText = comment
        container.appendChild(li)
      });
    } else {
      container.innerHTML = "<p>댓글이 없습니다.</p>"
    }

    // AI 분석
    if (data.ai_analysis) {
      const { temperature, summary } = data.ai_analysis
      const tempElement = document.getElementById("sentiment-score")
      document.getElementById("analysis-summary").innerText = summary
      tempElement.innerText = `${temperature}°`

      tempElement.style.color = temperature >= 70 ? "red" :
        temperature >= 40 ? "orange" : "blue"
    }

    // 즐겨찾기 상태
    const favorite = await authFetch("stocks", "favorites")
    favoriteBtn.innerText = favorite.favorites ? "💔즐겨찾기 취소" : "✨즐겨찾기"

    // 클릭 시 토글
    favoriteBtn.addEventListener("click", async () => {
      try {
        const res = await authFetch("stocks", `${name}/favorite`, "POST")
        alert(res.message)
        favoriteBtn.innerText = res.message.includes("추가") ? "💔즐겨찾기 취소" : "✨즐겨찾기"
      } catch (err) {
        console.error(err)
        alert("즐겨찾기 추가 실패")
      }
    });

  } catch (err) {
    console.error(err);
    container.innerHTML = "<p class='text-danger'>데이터를 불러올 수 없습니다.</p>"
    favoriteBtn.innerText = "✨즐겨찾기" // fallback
  }
})
