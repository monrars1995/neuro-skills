#!/usr/bin/env node

const { program } = require('commander');
const path = require('path');
const fs = require('fs-extra');
const chalk = require('chalk');
const inquirer = require('inquirer');
const ora = require('ora');

const VERSION = require('../package.json').version;
const SKILLS_DIR = path.join(__dirname, '..', 'skills');

// Agent directories for different AI CLIs
const AGENT_DIRS = {
  'claude-code': {
    name: 'Claude Code (Anthropic)',
    dir: path.join(require('os').homedir(), '.claude', 'skills')
  },
  'opencode': {
    name: 'OpenCode',
    dir: path.join(require('os').homedir(), '.opencode', 'skills')
  },
  'gemini-cli': {
    name: 'Gemini CLI (Google)',
    dir: path.join(require('os').homedir(), '.gemini', 'skills')
  },
  'codex': {
    name: 'OpenAI Codex',
    dir: path.join(require('os').homedir(), '.codex', 'skills')
  }
};

// Available skills
const SKILLS = [
  { id: 'meta-ads-manager', name: 'Meta Ads Manager', desc: 'Gerenciador completo de tráfego Meta Ads' },
  { id: 'traffic-strategist', name: 'Traffic Strategist', desc: 'Preparação e validação de campanhas' },
  { id: 'ad-copywriter', name: 'Ad Copywriter', desc: 'Copy on-brand para anúncios' },
  { id: 'neuro-ads-manager', name: 'Neuro Ads Manager', desc: 'CRUD, Analytics e Automação' },
  { id: 'agents', name: 'Vertical Agents', desc: 'Agentes especializados por vertical' }
];

program
  .name('neuro-skills')
  .description('O bastidor técnico que o mercado não mostra')
  .version(VERSION);

// Install command
program
  .command('install [skills...]')
  .description('Instala skills específicos ou todos')
  .option('-a, --agents <agent>', 'Agente alvo (claude-code, opencode, gemini-cli, codex)', 'claude-code')
  .option('-l, --list', 'Lista skills disponíveis')
  .action(async (skills, options) => {
    if (options.list) {
      console.log(chalk.blue('\n📦 Skills disponíveis:\n'));
      SKILLS.forEach(skill => {
        console.log(`  ${chalk.green('•')} ${chalk.bold(skill.name)}`);
        console.log(`    ${chalk.gray(skill.desc)}`);
      });
      return;
    }

    const agentDir = AGENT_DIRS[options.agents];
    if (!agentDir) {
      console.log(chalk.red(`\n❌ Agente "${options.agents}" não encontrado.`));
      console.log(chalk.gray('Agentes disponíveis: claude-code, opencode, gemini-cli, codex'));
      return;
    }

    const skillsToInstall = skills.length > 0 ? skills : 'all';
    
    console.log(chalk.blue('\n🧠 Neuro Skills - Instalação\n'));
    console.log(chalk.gray(`Agente: ${agentDir.name}`));
    console.log(chalk.gray(`Skills: ${skillsToInstall === 'all' ? 'Todos' : skillsToInstall.join(', ')}`));
    console.log();

    const spinner = ora('Instalando skills...').start();

    try {
      // Create directory if not exists
      await fs.ensureDir(agentDir.dir);

      // Copy skills
      if (skillsToInstall === 'all') {
        // Copy all skills
        const allSkills = SKILLS.map(s => s.id);
        for (const skill of allSkills) {
          const srcPath = path.join(SKILLS_DIR, skill);
          const destPath = path.join(agentDir.dir, skill);
          
          if (fs.existsSync(srcPath)) {
            await fs.copy(srcPath, destPath);
            console.log(chalk.green(`  ✓ ${skill} instalado`));
          }
        }
      } else {
        // Copy specific skills
        for (const skill of skillsToInstall) {
          const srcPath = path.join(SKILLS_DIR, skill);
          const destPath = path.join(agentDir.dir, skill);
          
          if (fs.existsSync(srcPath)) {
            await fs.copy(srcPath, destPath);
            console.log(chalk.green(`  ✓ ${skill} instalado`));
          } else {
            console.log(chalk.yellow(`  ⚠ ${skill} não encontrado`));
          }
        }
      }

      // Copy agent files if installing vertical agents
      if (skillsToInstall === 'all' || skillsToInstall.includes('agents')) {
        const agentsSrc = path.join(SKILLS_DIR, 'agents');
        const agentsDest = path.join(agentDir.dir, 'agents');
        if (fs.existsSync(agentsSrc)) {
          await fs.copy(agentsSrc, agentsDest);
          console.log(chalk.green('  ✓ Agentes verticais instalados'));
        }
      }

      spinner.succeed('Instalação concluída!');
      
      console.log(chalk.blue('\n✨ Próximos passos:'));
      console.log(chalk.gray('  1. Configure sua conta Meta Ads'));
      console.log(chalk.gray('  2. Execute: /meta-ads setup'));
      console.log(chalk.gray('  3. Crie sua primeira campanha'));
      console.log();
      console.log(chalk.cyan('📚 Documentação: https://goldneuron.io/'));
      console.log(chalk.cyan('📧 Newsletter: https://goldneuron.io/drops'));
      console.log(chalk.cyan('📸 Instagram: @monrars'));
      
    } catch (error) {
      spinner.fail('Erro na instalação');
      console.log(chalk.red(`\n❌ ${error.message}`));
      process.exit(1);
    }
  });

// Setup command
program
  .command('setup')
  .description('Configura uma nova instalação interativa')
  .action(async () => {
    console.log(chalk.blue('\n🧠 Neuro Skills - Setup Interativo\n'));
    
    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'agent',
        message: 'Qual agente você está usando?',
        choices: Object.entries(AGENT_DIRS).map(([key, value]) => ({
          name: value.name,
          value: key
        }))
      },
      {
        type: 'checkbox',
        name: 'skills',
        message: 'Quais skills você quer instalar?',
        choices: SKILLS.map(s => ({
          name: `${s.name} - ${chalk.gray(s.desc)}`,
          value: s.id,
          checked: true
        }))
      },
      {
        type: 'confirm',
        name: 'allVerticals',
        message: 'Instalar todos os agentes verticais?',
        default: true,
        when: (answers) => answers.skills.includes('agents')
      }
    ]);

    const agentDir = AGENT_DIRS[answers.agent];
    await fs.ensureDir(agentDir.dir);

    console.log();
    const spinner = ora('Instalando skills...').start();
    
    try {
      for (const skill of answers.skills) {
        const srcPath = path.join(SKILLS_DIR, skill);
        const destPath = path.join(agentDir.dir, skill);
        
        if (fs.existsSync(srcPath)) {
          // If agents skill, handle subdirectories
          if (skill === 'agents' && !answers.allVerticals) {
            // Copy only selected verticals
            const { verticals } = await inquirer.prompt([
              {
                type: 'checkbox',
                name: 'verticals',
                message: 'Quais verticais você quer?',
                choices: [
                  { name: '🚗 Concessionárias', value: 'concessionarias' },
                  { name: '🏠 Imobiliárias', value: 'imobiliarias' },
                  { name: '🛒 E-commerce', value: 'ecommerce' },
                  { name: '🎓 Educação', value: 'educacao' },
                  { name: '🏥 Saúde', value: 'saude' }
                ],
                default: ['concessionarias', 'ecommerce']
              }
            ]);
            
            await fs.ensureDir(destPath);
            for (const v of verticals) {
              const vSrc = path.join(srcPath, v);
              const vDest = path.join(destPath, v);
              if (fs.existsSync(vSrc)) {
                await fs.copy(vSrc, vDest);
              }
            }
          } else {
            await fs.copy(srcPath, destPath);
          }
          console.log(chalk.green(`  ✓ ${skill} instalado`));
        }
      }
      
      spinner.succeed('Setup concluído!');
      
      console.log(chalk.blue('\n✨ Instalação concluída!'));
      console.log(chalk.gray(`📁 Skills instalados em: ${agentDir.dir}`));
      console.log();
      console.log(chalk.cyan('📚 Documentação: https://goldneuron.io/'));
      console.log(chalk.cyan('📧 Newsletter: https://goldneuron.io/drops'));
      
    } catch (error) {
      spinner.fail('Erro no setup');
      console.log(chalk.red(`\n❌ ${error.message}`));
      process.exit(1);
    }
  });

// Uninstall command
program
  .command('uninstall [skills...]')
  .description('Remove skills instalados')
  .option('-a, --agents <agent>', 'Agente alvo', 'claude-code')
  .option('--all', 'Remove todos os skills')
  .action(async (skills, options) => {
    const agentDir = AGENT_DIRS[options.agents];
    if (!agentDir) {
      console.log(chalk.red(`\n❌ Agente "${options.agents}" não encontrado.`));
      return;
    }

    const spinner = ora('Removendo skills...').start();

    try {
      if (options.all) {
        await fs.remove(agentDir.dir);
        spinner.succeed('Todos os skills removidos!');
      } else {
        for (const skill of (skills.length > 0 ? skills : SKILLS.map(s => s.id))) {
          const skillPath = path.join(agentDir.dir, skill);
          if (fs.existsSync(skillPath)) {
            await fs.remove(skillPath);
          }
        }
        spinner.succeed('Skills removidos!');
      }
    } catch (error) {
      spinner.fail('Erro ao remover');
      console.log(chalk.red(`\n❌ ${error.message}`));
    }
  });

// List command
program
  .command('list')
  .description('Lista skills instalados')
  .option('-a, --agents <agent>', 'Agente alvo', 'claude-code')
  .action(async (options) => {
    const agentDir = AGENT_DIRS[options.agents];
    if (!agentDir) {
      console.log(chalk.red(`\n❌ Agente "${options.agents}" não encontrado.`));
      return;
    }

    console.log(chalk.blue(`\n📦 Skills instalados (${agentDir.name}):\n`));

    if (!fs.existsSync(agentDir.dir)) {
      console.log(chalk.gray('  Nenhum skill instalado.'));
      console.log(chalk.gray('  Execute: neuro-skills install'));
      return;
    }

    const installedSkills = fs.readdirSync(agentDir.dir);
    
    if (installedSkills.length === 0) {
      console.log(chalk.gray('  Nenhum skill instalado.'));
      console.log(chalk.gray('  Execute: neuro-skills install'));
      return;
    }

    installedSkills.forEach(skill => {
      const skillInfo = SKILLS.find(s => s.id === skill);
      const name = skillInfo ? skillInfo.name : skill;
      console.log(`  ${chalk.green('✓')} ${name}`);
    });

    console.log();
  });

// Version command
program
  .command('version')
  .description('Mostra versão instalada')
  .action(() => {
    console.log(chalk.blue(`\n🧠 Neuro Skills v${VERSION}\n`));
    console.log(chalk.gray('Site: https://goldneuron.io/'));
    console.log(chalk.gray('Newsletter: https://goldneuron.io/drops'));
    console.log(chalk.gray('Instagram: @monrars'));
    console.log();
  });

// Init command (creates project structure)
program
  .command('init [project-name]')
  .description('Cria estrutura de projeto')
  .option('-p, --path <path>', 'Caminho base', process.cwd())
  .action(async (projectName, options) => {
    const name = projectName || 'campanhas';
    const projectPath = path.join(options.path, name);
    
    console.log(chalk.blue('\n🧠 Neuro Skills - Criando Projeto\n'));
    
    const spinner = ora('Criando estrutura...').start();
    
    try {
      // Create directories
      await fs.ensureDir(projectPath);
      await fs.ensureDir(path.join(projectPath, 'clientes'));
      await fs.ensureDir(path.join(projectPath, 'templates'));
      
      // Create example structure
      const exampleClient = path.join(projectPath, 'clientes', 'exemplo');
      await fs.ensureDir(exampleClient);
      
      const exampleCampaign = path.join(exampleClient, '2024-01', 'black_friday');
      await fs.ensureDir(exampleCampaign);
      
      // Create example briefing
      const briefing = `# Briefing: Black Friday 2024

## Cliente
- **Nome:** Exemplo Corp
- **Produto:** Produto Exemplo
- **Indústria:** E-commerce

## Objetivos
- **Objetivo:** Vendas
- **CPA Alvo:** R$ 25
- **ROAS Alvo:** 4.0x
- **Orçamento:** R$ 50.000/mês

## Público-Alvo
- **Idade:** 25 a 45 anos
- **Localização:** Brasil
- **Interesses:** tecnologia, gadgets, ofertas

## Criativos
- 3 vídeos (Feed, Stories, Reels)
- 3 imagens (Feed, Stories)
`;
      
      await fs.writeFile(path.join(exampleCampaign, 'briefing.md'), briefing);
      
      // Create README
      const readme = `# ${name}

Estrutura de projeto para campanhas Meta Ads.

## Estrutura

\`\`\`
${name}/
├── clientes/
│   └── exemplo/
│       └── 2024-01/
│           └── black_friday/
│               ├── briefing.md
│               └── ad_*.{jpg,mp4}
└── templates/
\`\`\`

## Uso

1. Crie uma pasta para o cliente em \`clientes/\`
2. Crie uma pasta para a campanha com data
3. Adicione o \`briefing.md\`
4. Adicione os criativos (ad_01_feed_image.jpg, etc.)
5. Execute o neuro-skills

## Convenção de Nomes

\`\`\`
ad_{número}_{posicionamento}_{tipo}.{extensão}

ad_01_feed_image.jpg
ad_02_story_video.mp4
ad_03_reels_video.mp4
\`\`\`
`;
      
      await fs.writeFile(path.join(projectPath, 'README.md'), readme);
      
      spinner.succeed('Projeto criado!');
      
      console.log(chalk.blue('\n📁 Estrutura criada:'));
      console.log(chalk.gray(`  ${projectPath}`));
      console.log();
      console.log(chalk.cyan('📝 Próximos passos:'));
      console.log(chalk.gray('  1. Adicione briefing.md'));
      console.log(chalk.gray('  2. Adicione criativos'));
      console.log(chalk.gray('  3. Execute: neuro-skills analyze'));
      
    } catch (error) {
      spinner.fail('Erro ao criar projeto');
      console.log(chalk.red(`\n❌ ${error.message}`));
      process.exit(1);
    }
  });

// Info command
program
  .command('info')
  .description('Mostra informações do sistema')
  .action(() => {
    console.log(chalk.blue('\n🧠 Neuro Skills - Informações do Sistema\n'));
    
    console.log(chalk.bold('Versão:'), VERSION);
    console.log();
    
    console.log(chalk.bold('Skills:'));
    SKILLS.forEach(skill => {
      console.log(`  ${chalk.green('•')} ${skill.name}`);
      console.log(`    ${chalk.gray(skill.desc)}`);
    });
    
    console.log();
    console.log(chalk.bold('Agentes suportados:'));
    Object.entries(AGENT_DIRS).forEach(([key, value]) => {
      const exists = fs.existsSync(value.dir);
      const status = exists ? chalk.green('✓ instalado') : chalk.gray('não instalado');
      console.log(`  ${status} ${value.name}`);
    });
    
    console.log();
    console.log(chalk.cyan('📚 Links:'));
    console.log(chalk.gray('  Site: https://goldneuron.io/'));
    console.log(chalk.gray('  Newsletter: https://goldneuron.io/drops'));
    console.log(chalk.gray('  GitHub: https://github.com/monrars1995/neuro-skills'));
    console.log(chalk.gray('  Instagram: @monrars'));
    console.log();
  });

program.parse();