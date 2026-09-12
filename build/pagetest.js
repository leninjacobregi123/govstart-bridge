const {JSDOM,VirtualConsole}=require('jsdom'),fs=require('fs'),path=require('path');
const ROOT="/home/lenin/Apps Developed/SIH 26136/govstart-bridge";
const css=fs.readFileSync(path.join(ROOT,"assets/style.css"),"utf8");
const app=fs.readFileSync(path.join(ROOT,"assets/app.js"),"utf8");
const pages=fs.readdirSync(ROOT).filter(f=>f.endsWith(".html")).sort();
let pass=0,fail=0;
const ck=(l,c,x="")=>{c?(pass++):(fail++,console.log("  FAIL  "+l+(x?"  <- "+x:"")));};

// what each page must render, beyond the shared chrome
const EXPECT={
 "index.html":            ["#why .rev", ".hero h1", ".strip [data-count]"],
 "run-a-challenge.html":  ["#steps a", ".stage .card"],
 "where-it-runs.html":    ["#divGrid .divcard", ".photostrip .mphoto", ".warli-medallion"],
 "marketplace.html":      ["#mktGrid .lcard", "#catChips .chip"],
 "skills.html":           ["#skillPane .card"],
 "schemes.html":          ["#schemeList .lcard"],
 "skill-gap.html":        ["#gapBars .brow", "#gapCards .card"],
 "training.html":         ["#trainGrid .lcard", "#vidGrid .vid"],
 "resources.html":        ["#resPane .lcard"],
 "rule-book.html":        ["#ruleAcc .acc"],
 "judges-questions.html": ["#qaAcc .acc"],
 "help.html":             ["#helpAcc .acc"],
 "about.html":            ["#about .card"],
 "grievance.html":        ["#grvList", "#gv_txt"],
 "contact.html":          [".contact-grid .cbox"],
};
for(let i=1;i<=6;i++) EXPECT[`step-${i}-${["define-the-problem","cap-the-risk","see-whos-eligible","design-the-pilot","run-and-validate","buy-it-lawfully"][i-1]}.html`]=["#steps a","#railList dt",".pane"];

(async()=>{
for(const p of pages){
  const html=fs.readFileSync(path.join(ROOT,p),"utf8")
      .replace('<link rel="stylesheet" href="assets/style.css">',`<style>${css}</style>`)
      .replace('<script src="assets/app.js"></script>',`<script>${app}</script>`);
  const errs=[];const vc=new VirtualConsole();
  vc.on("jsdomError",e=>errs.push(e.message.split("\n")[0]));
  const dom=new JSDOM(html,{runScripts:"dangerously",pretendToBeVisual:true,url:"http://localhost/"+p,virtualConsole:vc});
  const d=dom.window.document;
  await new Promise(r=>setTimeout(r,60));
  ck(`${p}: no runtime errors`, errs.length===0, errs[0]);
  ck(`${p}: chrome present`, !!d.querySelector(".tricolour") && !!d.querySelector(".utility .emb")
     && !!d.querySelector("header.site nav") && !!d.querySelector("footer") && !!d.querySelector(".govfoot")
     && !!d.getElementById("aiP") && !!d.getElementById("modal"));
  const cur=d.querySelectorAll('#navlinks [aria-current="page"]');
  ck(`${p}: <=1 nav item marked current`, cur.length<=1, cur.length+" marked");
  for(const sel of (EXPECT[p]||[])){
    ck(`${p}: renders ${sel}`, d.querySelectorAll(sel).length>0);
  }
  dom.window.close();
}
console.log(`\n=== ${pass} passed, ${fail} failed across ${pages.length} pages ===`);
process.exit(fail?1:0);
})();
