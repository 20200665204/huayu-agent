# huayu_agent/agent.py
"""
华域 AI - 海外华人内容营销 Agent
HuaYu Agent: Overseas Chinese Content Marketing Automation
"""

import os
import json
import time
import random
import logging
from datetime import datetime
from typing import Optional
from openai import OpenAI  # moonshot uses openai-compatible API

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("HuaYuAgent")

MOONSHOT_BASE_URL = "https://api.moonshot.cn/v1"
MOONSHOT_MODEL = "moonshot-v1-8k"

PLATFORM_CONFIGS = {
    "tiktok": {
        "name": "TikTok",
        "max_chars": 150,
        "tags": ["#海外华人", "#短剧推荐", "#必看短剧", "#华人生活", "#海外生活"],
        "tone": "活泼、口语化、年轻化，使用emoji，制造悬念感",
    },
    "youtube": {
        "name": "YouTube",
        "max_chars": 500,
        "tags": ["#ChineseDrama", "#海外华人", "#短剧", "#OverseasChinese"],
        "tone": "信息丰富，有亲切感，适合搜索优化，包含简短故事介绍",
    },
    "instagram": {
        "name": "Instagram",
        "max_chars": 200,
        "tags": ["#华人", "#短剧推荐", "#海外生活", "#ChineseContent"],
        "tone": "精致、情感化，适合图文搭配，突出视觉感",
    },
    "xiaohongshu": {
        "name": "小红书",
        "max_chars": 300,
        "tags": ["#短剧", "#好剧推荐", "#海外华人必看", "#追剧"],
        "tone": "种草风格，像朋友分享，多用'姐妹'等称呼，真实感强",
    },
}

REGION_PERSONAS = {
    "southeast_asia": "居住在东南亚（新加坡/马来西亚/泰国）的华人，习惯繁简体混用，生活节奏快",
    "north_america": "居住在北美（美国/加拿大）的华人，思维偏西方但有中文内容需求，英文词汇偶尔混入",
    "australia_nz": "居住在澳大利亚/新西兰的华人，时差敏感，追求品质生活",
    "europe": "居住在欧洲的华人，中文内容相对匮乏，对优质中文内容渴望度高",
}


class ContentAgent:
    def __init__(self, api_key: str, base_url: str = MOONSHOT_BASE_URL):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.total_tokens = 0
        self.generated_count = 0
        logger.info("🌏 华域 AI Agent 初始化完成")

    def build_prompt(self, drama_info: dict, platform: str, region: str) -> str:
        config = PLATFORM_CONFIGS[platform]
        persona = REGION_PERSONAS.get(region, REGION_PERSONAS["southeast_asia"])
        return f"""你是一位专业的海外华人内容营销专家。
        
目标受众：{persona}
目标平台：{config['name']}（{config['tone']}）
字数限制：{config['max_chars']}字以内
平台标签：{' '.join(config['tags'])}

请为以下短剧/小说创作一篇推广文案：
- 作品名：{drama_info['title']}
- 类型：{drama_info['genre']}
- CPS平台：{drama_info.get('cps', '右豹平台')}
- 热度指数：{drama_info.get('hot_score', 90)}/100

要求：
1. 符合{config['name']}平台风格
2. 引发目标受众共鸣
3. 自然带入CPS推广链接入口（用[推广链接]占位）
4. 结尾加上平台标签
5. 不要有任何推销感，要像真实用户在分享

直接输出文案，不要任何解释。"""

    def generate_script(
        self,
        drama_info: dict,
        platform: str = "tiktok",
        region: str = "southeast_asia",
    ) -> Optional[dict]:
        logger.info(f"[Agent] 开始生成: {drama_info['title']} → {platform} ({region})")
        prompt = self.build_prompt(drama_info, platform, region)

        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=MOONSHOT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85,
                max_tokens=600,
            )
            elapsed = time.time() - start
            content = response.choices[0].message.content
            usage = response.usage
            self.total_tokens += usage.total_tokens
            self.generated_count += 1

            result = {
                "drama": drama_info["title"],
                "platform": platform,
                "region": region,
                "script": content,
                "tokens_used": usage.total_tokens,
                "elapsed_sec": round(elapsed, 2),
                "generated_at": datetime.now().isoformat(),
            }
            logger.info(f"[✓] 生成完成 | tokens: {usage.total_tokens} | 耗时: {elapsed:.2f}s")
            return result

        except Exception as e:
            logger.error(f"[✗] 生成失败: {e}")
            return None

    def batch_generate(self, dramas: list, platforms: list, regions: list) -> list:
        results = []
        total = len(dramas) * len(platforms) * len(regions)
        logger.info(f"[Agent] 批量任务启动: {total} 个内容待生成")

        for drama in dramas:
            for platform in platforms:
                for region in regions:
                    result = self.generate_script(drama, platform, region)
                    if result:
                        results.append(result)
                    time.sleep(0.5)  # rate limit protection

        logger.info(f"[Agent] 批量完成: {len(results)}/{total} | 总Token: {self.total_tokens:,}")
        return results

    def save_results(self, results: list, output_path: str = "output/scripts.json"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logger.info(f"[✓] 结果已保存至 {output_path}")


# --- Demo Run ---
if __name__ == "__main__":
    API_KEY = os.environ.get("MOONSHOT_API_KEY", "your_api_key_here")
    agent = ContentAgent(api_key=API_KEY)

    dramas = [
        {"title": "《错嫁豪门》", "genre": "豪门虐恋", "cps": "右豹平台", "hot_score": 98},
        {"title": "《重生之我是大佬》", "genre": "爽文逆袭", "cps": "番茄小说", "hot_score": 95},
    ]
    platforms = ["tiktok", "youtube"]
    regions = ["southeast_asia", "north_america"]

    results = agent.batch_generate(dramas, platforms, regions)
    agent.save_results(results)

    print(f"\n{'='*50}")
    print(f"✅ 华域 AI Agent 运行完毕")
    print(f"📄 生成内容: {agent.generated_count} 条")
    print(f"⚡ 消耗Token: {agent.total_tokens:,}")
    print(f"{'='*50}")
