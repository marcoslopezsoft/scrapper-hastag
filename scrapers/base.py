"""
Base models and abstract scraper definition for social media analytics.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod


@dataclass
class PostData:
    platform: str  # 'instagram', 'tiktok', 'x', 'facebook', 'cgera'
    id: str
    url: str
    author_username: str
    author_name: str
    text_content: str
    created_at: str  # ISO string or YYYY-MM-DD HH:MM:SS
    likes: int = 0
    comments: int = 0
    shares: int = 0
    views: int = 0
    media_type: str = "text"  # 'video', 'image', 'carousel', 'text'
    media_urls: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    is_official_cgera: bool = False
    location: Optional[str] = None
    sector: str = "Industria Nacional"
    raw_data: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_engagement(self) -> int:
        return self.likes + self.comments + self.shares

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["total_engagement"] = self.total_engagement
        return data


class BaseScraper(ABC):
    def __init__(self, hashtag: str = "queremostrabajar", timeout: int = 15):
        self.hashtag = hashtag.lstrip("#")
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "es-419,es;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    @abstractmethod
    def scrape(self, max_posts: int = 25) -> List[PostData]:
        """Scrape posts matching the hashtag."""
        pass

