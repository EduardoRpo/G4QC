# 📝 Instrucciones: Gitignore para .md y .html

## ✅ Cambio Aplicado

He agregado al `.gitignore`:
```
*.md
*.html
```

Esto significa que **todos los archivos .md y .html serán ignorados** por Git.

---

## 🔍 Verificar Estado

### Ver qué archivos .md y .html hay en el proyecto:
```powershell
Get-ChildItem -Recurse -Include *.md,*.html | Select-Object FullName
```

### Ver si Git los está rastreando:
```powershell
git ls-files | Select-String -Pattern "\.(md|html)$"
```

---

## 🗑️ Si Ya Están en el Repositorio

Si algunos archivos .md o .html **ya están siendo rastreados por Git**, necesitas removerlos del índice (pero mantenerlos localmente):

```powershell
# Remover del índice de Git (pero mantener archivos localmente)
git rm --cached *.md
git rm --cached *.html

# O remover recursivamente
git rm --cached -r **/*.md
git rm --cached -r **/*.html

# Luego hacer commit
git commit -m "Remove .md and .html files from tracking"
```

---

## ✅ Verificar que Funciona

### 1. Crear un archivo de prueba:
```powershell
echo "# Test" > test.md
```

### 2. Verificar que Git lo ignora:
```powershell
git status
```

**No debería aparecer `test.md` en los archivos modificados/nuevos.**

### 3. Limpiar el archivo de prueba:
```powershell
Remove-Item test.md
```

---

## 📋 Archivos que Serán Ignorados

Con esta configuración, estos archivos NO se subirán al repositorio:

- ✅ `README.md`
- ✅ `PROPUESTA_ARQUITECTURA.md`
- ✅ `PLAN_IMPLEMENTACION.md`
- ✅ `ARQUITECTURA_VISUAL.html`
- ✅ Todos los demás `.md` y `.html`

---

## ⚠️ Nota Importante

**Si necesitas mantener ALGÚN archivo .md o .html en el repositorio:**

Puedes usar una excepción en `.gitignore`:

```
# Ignorar todos los .md
*.md

# EXCEPTO este archivo específico
!README.md
```

---

## 🎯 Estado Actual

- ✅ `.gitignore` actualizado
- ✅ Archivos .md y .html serán ignorados
- ⏸️ Si ya están en Git, necesitas removerlos del índice (comandos arriba)

---

**¿Quieres que verifique si hay archivos ya rastreados que necesiten ser removidos?**

