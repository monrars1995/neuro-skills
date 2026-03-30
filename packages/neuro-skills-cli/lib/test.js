#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const NEURO_DIR = path.join(os.homedir(), '.neuro-skills');
const SKILLS_DIR = path.join(NEURO_DIR, 'skills');
const CONFIG_FILE = path.join(NEURO_DIR, 'config.json');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (err) {
    console.log(`❌ ${name}: ${err.message}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function main() {
  console.log('\n🧪 Neuro Skills - Test Suite\n');
  
  test('Home directory exists', () => {
    assert(fs.existsSync(NEURO_DIR), `${NEURO_DIR} should exist`);
  });
  
  test('Skills directory exists', () => {
    assert(fs.existsSync(SKILLS_DIR), `${SKILLS_DIR} should exist`);
  });
  
  test('Config file exists', () => {
    assert(fs.existsSync(CONFIG_FILE), `${CONFIG_FILE} should exist`);
  });
  
  test('Config is valid JSON', () => {
    const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
    assert(config.version, 'Config should have version');
    assert(config.creator, 'Config should have creator');
    assert(config.site, 'Config should have site');
  });
  
  test('Core skills installed', () => {
    const coreSkills = ['meta-ads-manager', 'traffic-strategist', 'ad-copywriter', 'neuro-ads-manager'];
    coreSkills.forEach(skill => {
      const skillDir = path.join(SKILLS_DIR, skill);
      assert(fs.existsSync(skillDir), `Skill ${skill} should be installed`);
    });
  });
  
  test('Vertical skills installed', () => {
    const verticals = ['concessionarias', 'imobiliarias', 'ecommerce', 'educacao', 'saude'];
    verticals.forEach(vertical => {
      const verticalDir = path.join(SKILLS_DIR, vertical);
      assert(fs.existsSync(verticalDir), `Vertical ${vertical} should be installed`);
    });
  });
  
  test('SKILL.md files present', () => {
    const allSkills = ['meta-ads-manager', 'traffic-strategist', 'ad-copywriter', 'neuro-ads-manager',
                       'concessionarias', 'imobiliarias', 'ecommerce', 'educacao', 'saude'];
    allSkills.forEach(skill => {
      const skillFile = path.join(SKILLS_DIR, skill, 'SKILL.md');
      assert(fs.existsSync(skillFile), `${skill}/SKILL.md should exist`);
    });
  });
  
  console.log('\n📊 Test Results\n');
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📋 Total: ${passed + failed}\n`);
  
  if (failed > 0) {
    process.exit(1);
  }
  
  console.log('✨ All tests passed!\n');
}

main();