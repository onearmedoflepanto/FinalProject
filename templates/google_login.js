document.getElementById("google-login").addEventListener("click", () => {
  const clientId = "1073818362571-jk8j30h4o317n8bfaqophaqeqj3bhddi.apps.googleusercontent.com";
  const redirectUri = "http://localhost:8001/api/accounts/google/callback/";
  const scope = "openid email profile";

  const oauthUrl = `https://accounts.google.com/o/oauth2/v2/auth?` +
    `client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&response_type=code` +
    `&scope=${encodeURIComponent(scope)}`;

  window.location.href = oauthUrl;
});