#!/usr/bin/env node

/**
 * Convert Markdown files to Gemtext format
 * Usage: node convert-to-gemtext.js input.md output.gmi
 */

const fs = require('fs');
const path = require('path');

function convertMarkdownToGemtext(markdown) {
  let gemtext = markdown;
  
  // Convert headings (# -> ##, ## -> ###, ### -> ####, then remove extra #)
  gemtext = gemtext.replace(/^#### (.+)$/gm, '### $1');
  gemtext = gemtext.replace(/^### (.+)$/gm, '## $1');
  gemtext = gemtext.replace(/^## (.+)$/gm, '# $1');
  gemtext = gemtext.replace(/^# (.+)$/gm, '# $1');
  
  // Convert lists (- or * to *)
  gemtext = gemtext.replace(/^[\-\*] (.+)$/gm, '* $1');
  
  // Convert blockquotes (> to >)
  gemtext = gemtext.replace(/^> (.+)$/gm, '> $1');
  
  // Convert code blocks to preformatted text
  gemtext = gemtext.replace(/```[\s\S]*?```/g, (match) => {
    const content = match.replace(/```\n?/g, '').replace(/```\n?$/g, '');
    return '```\n' + content + '\n```';
  });
  
  // Convert inline code to preformatted text
  gemtext = gemtext.replace(/`([^`]+)`/g, '```\n$1\n```');
  
  // Convert markdown links [text](url) to gemtext links => url text
  gemtext = gemtext.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '=> $2 $1');
  
  // Remove bold and italic markup
  gemtext = gemtext.replace(/\*\*([^*]+)\*\*/g, '$1');
  gemtext = gemtext.replace(/\*([^*]+)\*/g, '$1');
  gemtext = gemtext.replace(/__([^_]+)__/g, '$1');
  gemtext = gemtext.replace(/_([^_]+)_/g, '$1');
  
  // Remove images (convert to links)
  gemtext = gemtext.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '=> $2 $1');
  
  return gemtext;
}

function main() {
  const inputFile = process.argv[2];
  const outputFile = process.argv[3];
  
  if (!inputFile || !outputFile) {
    console.log('Usage: node convert-to-gemtext.js input.md output.gmi');
    process.exit(1);
  }
  
  try {
    const markdown = fs.readFileSync(inputFile, 'utf8');
    const gemtext = convertMarkdownToGemtext(markdown);
    fs.writeFileSync(outputFile, gemtext, 'utf8');
    console.log(`Converted ${inputFile} to ${outputFile}`);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { convertMarkdownToGemtext };
