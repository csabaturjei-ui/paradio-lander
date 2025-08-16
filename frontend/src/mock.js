// Mock data and functions for Post Apocalyptic Radio

export const mockEmailSignup = (email) => {
  console.log('Mock: Email signup submitted:', email);
  // Simulate API call delay
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: 'Successfully joined the waitlist!'
      });
    }, 1000);
  });
};

export const features = [
  {
    id: 1,
    title: "Artist-Owned Music, Powered by IPFS",
    description: "Instead of uploading music to a corporate server, artists directly control their content. They upload their songs to IPFS (InterPlanetary File System) - a global, decentralized hard drive where files are stored across many computers, making them more resilient and censorship-resistant.",
    icon: "Music"
  },
  {
    id: 2,
    title: "Solana Blockchain for Trust & Transparency", 
    description: "All the important information about songs (artist, title, the IPFS link to the song) is immutably recorded on the Solana blockchain. When the artist uploads a song, a record of it goes onto Solana, visible to everyone.",
    icon: "Shield"
  },
  {
    id: 3,
    title: "Social Discovery: \"Ping with a Song\"",
    description: "Forget black-box algorithms! On P.A.R., you discover music through your friends and the community. Our unique \"Ping with a Song\" feature lets you directly send a song recommendation to another user.",
    icon: "Zap"
  },
  {
    id: 4,
    title: "Community-Driven \"Most Pinged Radio\"",
    description: "Want to know what's hot right now in the P.A.R. universe? Tune into the \"Most Pinged Radio.\" This feature automatically compiles a playlist of the songs that have been \"pinged\" (shared) the most by users within a recent timeframe.",
    icon: "Radio"
  },
  {
    id: 5,
    title: "Future of Incentives with a Custom Solana Token",
    description: "While not fully implemented in this early prototype, the vision for P.A.R. includes a custom Solana token. This token will be used to reward artists for their creations and incentivize listeners who actively participate, share, and even help \"seed\" (host) music on the IPFS network.",
    icon: "Coins"
  }
];

export const socialLinks = [
  { name: 'Twitter', icon: 'Twitter', url: 'https://x.com/postapradio' },
  { name: 'TikTok', icon: 'Music', url: 'https://tiktok.com/@postapradio' },
  { name: 'Discord', icon: 'MessageCircle', url: 'https://discord.gg/f2M7tuVe' },
  { name: 'Instagram', icon: 'Instagram', url: 'https://instagram.com/postapocalypticradio' }
];

export const kofiUrl = 'https://ko-fi.com/postapocalypticradio';