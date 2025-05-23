import { authFetch } from "./api.js";

const DETAIL_URL = "http://127.0.0.1:8000/detail/"

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("stock-list")
  const favoriteContainer = document.getElementById("stock-favorite")

  try {
    const hotStocks = await authFetch("stocks", "hot")
    hotStocks.forEach(stock => {
      container.innerHTML += `
        <div class="col">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">${stock.name}</h5>
              <p class="card-text">💵 ${stock.price}</p>
              <p class="card-text">📈 ${stock.change}</p>
              <a href="${DETAIL_URL}${stock.name}/" class="btn btn-primary">자세히</a>
            </div>
          </div>
        </div>`
    })

    const favoriteStocks = await authFetch("stocks", "favorites")
    favoriteStocks.forEach(stock => {
      favoriteContainer.innerHTML += `
        <div class="col">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">${stock.name}</h5>
              <p class="card-text">💵 ${stock.price}</p>
              <p class="card-text">📈 ${stock.change}</p>
              <a href="${DETAIL_URL}${stock.name}/" class="btn btn-primary">자세히</a>
            </div>
          </div>
        </div>`
    })

  } catch (err) {
    container.innerHTML = `<p class="text-danger">데이터 로딩 실패</p>`
    console.log('데이터 로딩 실패.', err)
  }
});
