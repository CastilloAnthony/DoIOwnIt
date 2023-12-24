{"npsso":"6aAFJd53dTJLVmtUXmwsOjgQYpiQZM1OfWk7L8O8CQ1XfAEOwcZVntp3gYbdkvCy"}

// This is the value you copied from the previous step.
const myNpsso = "<64 character token>";

// We'll exchange your NPSSO for a special access code.
const accessCode = await exchangeNpssoForCode(npsso);

// 🚀 We can use the access code to get your access token and refresh token.
const authorization = await exchangeCodeForAccessToken(accessCode);