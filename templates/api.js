export async function authFetch(path1, path2 = '', path3 = '', mode = 'GET', bodyData = null, showAlertOnError = true, retryCount = 0) {
  if (retryCount > 3) {
    return refreshError()
  }
  const API_BASE = 'http://127.0.0.1:8001/api'
  const access = localStorage.getItem("access");
  const url = [API_BASE, path1, path2, path3].filter(Boolean).join("/");

  const options = {
    method: mode,
    headers: {
      "Content-Type": "application/json",
      ...(access && { "Authorization": `Bearer ${access}` })
    }
  };

  if (bodyData) {
    options.body = JSON.stringify(bodyData);
  }

  try {
    const res = await fetch(url, options);

    if (res.status === 401 && access) {
      const refreshed = await tokenRefresh();
      if (refreshed) {
        return await authFetch(path1, path2, mode, bodyData, showAlertOnError);
      }
    }

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      const msg = data.error || data.message || "요청 실패";
      if (showAlertOnError) alert(msg);
      throw new Error(msg);
    }

    const contentType = res.headers.get("Content-Type");
    return contentType && contentType.includes("application/json")
      ? await res.json()
      : await res.text();
  } catch (err) {
    console.error(`서버 오류: ${url}`, err);
    if (showAlertOnError) alert("서버 오류");
    throw err;
  }
}

async function tokenRefresh() {
  const refreshUrl = 'http://127.0.0.1:8001/api/accounts/refresh/';
  const refresh = localStorage.getItem("refresh");

  if (!refresh) return refreshError();

  try {
    const res = await fetch(refreshUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh })
    });

    if (!res.ok) return refreshError();

    const data = await res.json();
    if (data.access) {
      localStorage.setItem("access", data.access);
      return data.access;
    }
    return refreshError();
  } catch (err) {
    return refreshError();
  }
}

function refreshError() {
  alert('인증 오류가 발생하였습니다. 로그아웃 후 다시 로그인 해주세요.');
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  location.href = "/login/";
  return null;
}

export function getCurrentUserId() {
  try {
    const token = localStorage.getItem("access");
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id;
  } catch {
    return null;
  }
}

async function nonAuthFetch(path1, path2 = '', path3 = '', mode = 'GET', bodyData = null, showAlertOnError = true) {
  const API_BASE = 'http://127.0.0.1:8001/api'
  const url = [API_BASE, path1, path2, path3].filter(Boolean).join("/");

  const options = {
    method: mode,
    headers: {
      "Content-Type": "application/json"
    }
  }
  if (bodyData) {
    options.body = JSON.stringify(bodyData);
  }

  try {
    const res = await fetch(url, options);

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      const msg = data.error || data.message || "요청 실패";
      if (showAlertOnError) alert(msg);
      throw new Error(msg);
    }

    const contentType = res.headers.get("Content-Type");
    return contentType && contentType.includes("application/json")
      ? await res.json()
      : await res.text();
  } catch (err) {
    console.error(`서버 오류: ${url}`, err);
    if (showAlertOnError) alert("서버 오류");
    throw err;
  }
}