function validar() {
  const email = document.getElementById("email").value;
  const opcion = document.querySelector('input[name="opcion"]:checked');

  if (email.length < 7 || email[0] === '@' || email[email.length - 1] === '@' ||
      email[0] === '.' || email[email.length - 1] === '.' ||
      !email.includes('@') || !email.includes('.') ||
      /[#\$%\*!]/.test(email)) {
    alert("Email inválido");
    return false;
  }

  if (!opcion) {
    alert("Debe seleccionar una opción");
    return false;
  }

  return true;
}
