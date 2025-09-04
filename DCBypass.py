import requests, threading, os, fake_headers, colorama
colorama.init(autoreset=True)

def read_proxy_list(filename):
    with open(filename, 'r') as file:
        return [{"https": "http://" + line.strip()} for line in file]

def split_list(lst, num_chunks):
    avg = len(lst) / float(num_chunks)
    return [lst[int(i * avg):int((i + 1) * avg)] for i in range(num_chunks)]

def DCRequest(url, proxies_chunk):
    for proxy_info in proxies_chunk:
        proxy = {"https": proxy_info['https']}
        usingProxy = proxy_info['https'].split('//')[1]

        try:
            r = requests.get(url, headers=fake_headers.Headers(browser='chrome', os='win', headers=True).generate(), proxies=proxy, timeout=10)
            if r.status_code == 200 and "Success!" in r.text:
                print(f"✅ {colorama.Fore.GREEN}Successfully bypassed DC, please wait a few seconds... | Proxy: {usingProxy}")
                os._exit(0)
            elif "Expired link" in r.text:
                print(f"⚠️ {colorama.Fore.YELLOW}URL is expired, use a new link | Proxy: {usingProxy}")
                os._exit(0)
            elif "RR02" in r.text:
                print(f"🚫 {colorama.Fore.YELLOW}DC detected the alt account, use a new link | Proxy: {usingProxy}")
                os._exit(0)
            elif "RV01" in r.text:
                print(f"🚫 {colorama.Fore.YELLOW}DC detected the proxy | Proxy: {usingProxy}")
            else:
                print(f"🚫 {colorama.Fore.MAGENTA}Blocked by Cloudflare | Proxy: {usingProxy}")
        except:
            print(f"❌ {colorama.Fore.RED}Proxy error | Proxy: {usingProxy}")
        
        threadLock.acquire()
        try:
            with open('proxies.txt', 'r') as file:
                lines = file.readlines()
            with open('proxies.txt', 'w') as file:
                for line in lines:
                    if line.strip("\n") != usingProxy:
                        file.write(line)
        finally:
            threadLock.release()

if __name__ == "__main__":
    url = input("DC verify url: ")
    proxies_list = read_proxy_list("proxies.txt")
    num_threads = "5"
    proxies_chunks = split_list(proxies_list, num_threads)

    threadLock = threading.Lock()
    threads = [threading.Thread(target=DCRequest, args=(url, chunk)) for chunk in proxies_chunks]
    [thread.start() for thread in threads]

    [thread.join() for thread in threads]
