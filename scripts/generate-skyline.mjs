// Generates skyline.svg (animated 3D-style skyline of your contribution calendar).
// Output goes to the repo root, next to contrib-heatmap.svg / whoami.svg / stats.svg.
import { writeFileSync } from "node:fs";

const login = process.env.GH_LOGIN || "SubhamPro11";
const token = process.env.GITHUB_TOKEN;
if (!token) throw new Error("Set GITHUB_TOKEN");

const query = `query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{date weekday contributionCount}}}}}}`;
const res = await fetch("https://api.github.com/graphql", {
  method: "POST",
  headers: { Authorization: `bearer ${token}`, "Content-Type": "application/json" },
  body: JSON.stringify({ query, variables: { login } }),
});
const json = await res.json();
if (!json.data?.user) throw new Error("GitHub API error: " + JSON.stringify(json));
const weeks = json.data.user.contributionsCollection.contributionCalendar.weeks;

// quartile levels from non-zero days
const all = weeks.flatMap((w) => w.contributionDays.map((d) => d.contributionCount));
const nz = all.filter((x) => x > 0).sort((a, b) => a - b);
const q = [0.25, 0.5, 0.75].map((p) => nz[Math.floor(nz.length * p)] ?? 1);
const level = (n) => (n === 0 ? 0 : n <= q[0] ? 1 : n <= q[1] ? 2 : n <= q[2] ? 3 : 4);
const maxc = Math.max(1, ...all);

// Palette matches the profile: dark card #181b19, accent #9bbf7a
const BG = "#181b19";
const PAL = ["#262c27", "#3c5535", "#5d8050", "#7ea565", "#a3cc80"];

function shade(hex, f) {
  const v = parseInt(hex.slice(1), 16);
  const t = f > 0 ? 255 : 0, k = Math.abs(f);
  const m = (c) => Math.round(c + (t - c) * k);
  return `rgb(${m(v >> 16)},${m((v >> 8) & 255)},${m(v & 255)})`;
}

const W = 860, H = 340, pad = 22, N = weeks.length;
const c = (W - pad * 2) / (N + 0.45), o = c * 0.45, bw = c * 0.8, step = c * 0.95;
const y0 = H * 0.9 - 6 * step;
const k = Math.min(y0 - o - 6, H * 0.55) / Math.sqrt(maxc);
const f = (n) => n.toFixed(1);

let out = "";
for (let r = 0; r < 7; r++) {            // back row first, front row last
  weeks.forEach((wk, w) => {
    const d = wk.contributionDays.find((x) => x.weekday === r);
    if (!d) return;
    const h = Math.max(1.5, Math.sqrt(d.contributionCount) * k);
    const x = pad + w * c, y = y0 + r * step + o;
    const base = PAL[level(d.contributionCount)];
    const delay = ((6 - r) * 0.11 + w * 0.014).toFixed(3);
    out += `<g class="b" style="animation-delay:${delay}s"><title>${d.contributionCount} on ${d.date}</title>` +
      `<rect x="${f(x)}" y="${f(y - h)}" width="${f(bw)}" height="${f(h)}" fill="${base}"/>` +
      `<polygon points="${f(x)},${f(y - h)} ${f(x + bw)},${f(y - h)} ${f(x + bw + o)},${f(y - h - o)} ${f(x + o)},${f(y - h - o)}" fill="${shade(base, 0.3)}"/>` +
      `<polygon points="${f(x + bw)},${f(y - h)} ${f(x + bw + o)},${f(y - h - o)} ${f(x + bw + o)},${f(y - o)} ${f(x + bw)},${f(y)}" fill="${shade(base, -0.3)}"/></g>`;
  });
}

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<style>.b{transform-box:fill-box;transform-origin:50% 100%;animation:rise .7s cubic-bezier(.34,1.56,.64,1) both}
@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@media (prefers-reduced-motion:reduce){.b{animation:none}}</style>
<rect width="${W}" height="${H}" rx="12" fill="${BG}"/>${out}</svg>`;

writeFileSync("skyline.svg", svg);
console.log("Wrote skyline.svg");
