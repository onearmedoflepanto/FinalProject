function setupNavbar() {
  const isLoggedIn = !!localStorage.getItem("access")

  document.getElementById("nav-login").classList.toggle("d-none", isLoggedIn);
  document.getElementById("nav-signup").classList.toggle("d-none", isLoggedIn);
  document.getElementById("nav-mypage").classList.toggle("d-none", !isLoggedIn);
  document.getElementById("nav-logout").classList.toggle("d-none", !isLoggedIn);

  window.logout = () => {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    alert("로그아웃 되었습니다.")
    location.href = "/"
  }
}

function setupSearch() {
  const form = document.getElementById("stock-search-form")
  if (!form) return;
  form.addEventListener("submit", (event) => {
    event.preventDefault()
    const query = document.getElementById("search-input").value.trim()
    if (query) {
      location.href = `/detail/${encodeURIComponent(query)}`
    }
  })
}

async function loadNavbar() {
  const placeholder = document.createElement("div")
  placeholder.id = "navbar-placeholder"
  document.body.prepend(placeholder)

  try {
    const res = await fetch("/static/components/navbar.html")
    if (!res.ok) throw new Error("네비게이션 로딩에 문제가 있습니다. 페이지를 새로고침 해주세요.")
    const html = await res.text()
    placeholder.outerHTML = html
    setupNavbar()
    setupSearch()
  }
  catch (err) {
    console.error("네비게이션 로딩 오류", err)
  }
}

async function dynamicImportScript(path) {
  try {
    await import(path);
  } catch (err) {
    console.error(`모듈 로딩 실패: ${path}`, err);
  }
}

async function loadPageModules() {
  const path = window.location.pathname

  if (path === "/" || path === "/index.html") {
    await dynamicImportScript("./index.js");
  } else if (path.includes("/login")) {
    await dynamicImportScript("./login.js");
    await dynamicImportScript("./google_login.js");
  } else if (path.includes("/sign_up")) {
    await dynamicImportScript("./sign_up.js");
  } else if (path.includes("/mypage")) {
    await dynamicImportScript("./mypage.js");
  } else if (path.includes("/detail/")) {
    await dynamicImportScript("./get_stock_detail.js");
    await dynamicImportScript("./get_board.js");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadNavbar()
  await loadPageModules()
}) 