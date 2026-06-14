export const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export const validateText = (name) => {
    if (name.trim() !== name) {
        return false;
    }
    const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

    return regex.test(name);
}

export const validatePassword = (password) => {
    if (password.trim().length <= 8) {
        return false;
    }
    return true;
}