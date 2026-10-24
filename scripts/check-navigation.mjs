import assert from 'node:assert/strict'
import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { resolve, extname } from 'node:path'
import { chromium } from 'playwright-chromium'

// Server statico senza fallback SPA, come GitHub Pages in un sottopercorso.
const prefix = '/linuxday2026-platformio/'
const root = resolve('dist')
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml' }
const server = createServer(async (req, res) => {
  const path = new URL(req.url, 'http://localhost').pathname
  const file = resolve(root, path.slice(prefix.length) || 'index.html')
  if (!path.startsWith(prefix) || !file.startsWith(`${root}/`)) {
    res.writeHead(404).end()
    return
  }
  try {
    const data = await readFile(file)
    res.writeHead(200, { 'Content-Type': mime[extname(file)] || 'application/octet-stream' }).end(data)
  }
  catch { res.writeHead(404).end() }
})
await new Promise(r => server.listen(0, '127.0.0.1', r))
const origin = `http://127.0.0.1:${server.address().port}`
const browser = await chromium.launch({ headless: true })
try {
  for (const viewport of [{ width: 390, height: 844 }, { width: 844, height: 390 }, { width: 1280, height: 800 }]) {
    const mobile = viewport.width !== 1280
    const context = await browser.newContext({ viewport, hasTouch: mobile, isMobile: mobile })
    const page = await context.newPage()
    await page.goto(origin + prefix)
    // La ricerca chiusa non deve lasciare l’elenco dei titoli sulla slide.
    const search = page.locator('#slidev-goto-dialog')
    await search.locator('input:disabled').waitFor({ state: 'attached' })
    assert.equal(await search.isVisible(), false)
    if (mobile)
      await page.screenshot({ path: `/tmp/linuxday-slide-${viewport.width}.png` })
    if (!mobile) {
      await page.keyboard.press('g')
      await search.waitFor({ state: 'visible' })
      await search.locator('input').fill('PlatformIO')
      await search.locator('.autocomplete-list').waitFor({ state: 'visible' })
      await page.keyboard.press('Escape')
      await search.waitFor({ state: 'hidden' })
    }
    const overview = page.getByTitle('Show slide overview', { exact: true })
    if (mobile) await overview.tap()
    else { await overview.hover(); await overview.click() }
    const card = page.locator('.z-modal .grid > div').nth(4).locator('.slidev-slide-container').first()
    // Il contenitore interno non riceve eventi; selezionare la miniatura esterna.
    const target = page.locator('.z-modal .grid > div').nth(4).locator(':scope > div').first()
    await card.waitFor({ state: 'visible' })
    if (mobile) await target.tap()
    else await target.click()
    await page.waitForURL(`${origin}${prefix}#/5`)
    await page.locator('.z-modal > .grid').waitFor({ state: 'hidden' })
    // Anche la slide corrente deve chiudere l’indice, senza cambiare URL.
    if (mobile) await overview.tap()
    else await overview.click()
    await target.waitFor({ state: 'visible' })
    if (mobile) await target.tap()
    else await target.click()
    await page.locator('.z-modal > .grid').waitFor({ state: 'hidden' })
    if (mobile) await overview.tap()
    else await overview.click()
    const close = page.getByTitle('Close', { exact: true })
    await close.waitFor({ state: 'visible' })
    if (mobile) {
      const bounds = await close.boundingBox()
      assert.ok(bounds.width >= 48 && bounds.height >= 48)
      assert.ok(bounds.x >= 0 && bounds.y >= 0)
      assert.ok(bounds.x + bounds.width <= viewport.width)
      assert.ok(bounds.y + bounds.height <= viewport.height)
      await page.screenshot({ path: `/tmp/linuxday-indice-${viewport.width}.png` })
    }
    if (mobile) await close.tap()
    else await close.click()
    await page.locator('.z-modal > .grid').waitFor({ state: 'hidden' })
    assert.equal((await page.reload()).status(), 200)
    await page.getByTitle('Show slide overview', { exact: true }).waitFor()
    assert.equal(new URL(page.url()).hash, '#/5')
    assert.equal(await search.isVisible(), false)
    console.log(`Navigazione e ricaricamento OK: ${viewport.width}×${viewport.height}`)
    await context.close()
  }
}
finally { await browser.close(); await new Promise(r => server.close(r)) }
