#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const NEURO_DIR = path.join(os.homedir(), '.neuro-skills');
const SKILLS_DIR = path.join(NEURO_DIR, 'skills');
const CONFIG_FILE = path.join(NEURO_DIR, 'config.json');

console.log('\n🧠 Neuro Skills - Post-installation setup\n');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`✅ Created: ${dir}`);
  }
}

function createDefaultConfig() {
  const defaultConfig = {
    version: require('../package.json').version,
    installedAt: new Date().toISOString(),
    creator: '@monrars',
    site: 'https://goldneuron.io/',
    community: 'https://goldneuron.io/drops',
    agentHost: 'localhost',
    agentPort: 8501,
    verticals: ['concessionarias', 'imobiliarias', 'ecommerce', 'educacao', 'saude']
  };

  if (!fs.existsSync(CONFIG_FILE)) {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(defaultConfig, null, 2));
    console.log(`✅ Created config: ${CONFIG_FILE}`);
  }
}

function copySkillsToHome() {
  const packageSkillsDir = path.join(__dirname, '..', 'skills');
  
  if (fs.existsSync(packageSkillsDir)) {
    ensureDir(SKILLS_DIR);
    
    const verticals = ['meta-ads-manager', 'traffic-strategist', 'ad-copywriter', 'neuro-ads-manager',
                       'concessionarias', 'imobiliarias', 'ecommerce', 'educacao', 'saude'];
    
    verticals.forEach(vertical => {
      const srcDir = path.join(packageSkillsDir, vertical);
      const destDir = path.join(SKILLS_DIR, vertical);
      
      if (fs.existsSync(srcDir)) {
        ensureDir(destDir);
        
        const files = fs.readdirSync(srcDir);
        files.forEach(file => {
          const srcFile = path.join(srcDir, file);
          const destFile = path.join(destDir, file);
          fs.copyFileSync(srcFile, destFile);
        });
        console.log(`✅ Copied skills: ${vertical}`);
      }
    });
  }
}

function main() {
  console.log('📁 Setting up directories...\n');
  
  ensureDir(NEURO_DIR);
  ensureDir(SKILLS_DIR);
  
  console.log('\n📝 Creating configuration...\n');
  createDefaultConfig();
  
  console.log('\n📋 Copying skills to home directory...\n');
  copySkillsToHome();
  
  console.log('\n✨ Neuro Skills installed successfully!\n');
  console.log('Run `neuro-skills start` to launch the agent.');
  console.log('Run `neuro-skills --help` for available commands.\n');
  console.log('📚 Documentation: https://goldneuron.io/');
  console.log('💬 Community: https://goldneuron.io/drops\n');
}

main();