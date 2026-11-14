import base64, json, re, subprocess, sys, time
from pathlib import Path
ACC="91c5bf467d30ea7e0c866ee7bcfd1e6f"
OUT=Path(__file__).resolve().parent
def token():
    t=(Path.home()/"Library/Preferences/.wrangler/config/default.toml").read_text()
    return re.search(r'oauth_token = "([^"]+)"',t).group(1)
S=", photorealistic editorial photograph, natural daylight, no people, no text, no signs, no logos"
J={
"priestory":("Bright empty commercial retail space for rent, large shop-front windows, light concrete floor, white walls, spotlights on ceiling, clean and ready to move in, eye-level wide view"+S,1792,1024),
"kancelaria":("Modern empty office space for rent in a small town building, light wooden floor, white walls, tall windows, a few ceiling lights, calm and tidy, wide view"+S,1536,1024),
"poziconva":("Neatly organised rental storage room with shelves holding folding tables, stacked chairs, a ladder and plastic crates, light grey walls, tidy equipment rental warehouse"+S,1536,1024),
}
for n in (sys.argv[1:] or J):
    p,w,h=J[n]; out=OUT/f"{n}.jpg"
    if out.exists(): continue
    for a in range(3):
        r=subprocess.run(["curl","-s","-m","240","-X","POST",f"https://api.cloudflare.com/client/v4/accounts/{ACC}/ai/run/@cf/black-forest-labs/flux-2-dev","-H",f"Authorization: Bearer {token()}","-F",f"prompt={p}","-F",f"width={w}","-F",f"height={h}"],capture_output=True,text=True)
        try:
            d=json.loads(r.stdout)
            if d.get("success") and d["result"].get("image"):
                out.write_bytes(base64.b64decode(d["result"]["image"])); print("ok",n); break
            print("err",n,d.get("errors"))
        except Exception as e: print("err",n,r.stdout[:150])
        time.sleep(10)
