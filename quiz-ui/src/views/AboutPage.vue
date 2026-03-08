<template>
  <div class="page-wrap fade-up">
    <div class="about-hero">
      <div class="about-emoji">🎓</div>
      <h1>À propos du projet</h1>
      <p class="about-sub">Quiz de culture générale cognitique</p>
    </div>
    <div class="about-sections">
      <div class="section-card card">
        <h2> Qu'est-ce que ce projet ?</h2>
        <p>Ce projet est une application de quiz interactif axée sur la culture générale et les sciences cognitiques. Conçu pour tester et enrichir vos connaissances, il offre une expérience ludique et engageante.</p>
      </div>
      <div class="section-card card">
        <h2> Auteurs</h2>
        <div class="authors">
          <div class="author-row">
            <span class="author-avatar">👤</span>
            <div>
              <strong>Mame Awa Ndiaye</strong>
              <p>Développeuse informatique.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="section-card card">
        <h2> Pourquoi ce projet ?</h2>
        <p>Projet étudiant dans le cadre de la matière développement web. L'objectif est de répondre aux besoins du cahier des charges et de créer une application scalable.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-wrap { max-width: 640px; margin: 0 auto; padding: 40px 20px; }
.about-hero { text-align: center; margin-bottom: 32px; }
.about-emoji { font-size: 80px; display: block; margin-bottom: 12px; }
.about-hero h1 { font-size: 1.8rem; font-weight: 900; }
.about-sub { color: var(--text-mid); font-size: 15px; margin-top: 4px; }
.about-sections { display: flex; flex-direction: column; gap: 16px; }
.section-card h2 { font-size: 1rem; font-weight: 900; margin-bottom: 10px; }
.section-card p { color: var(--text-mid); font-size: 14px; line-height: 1.7; }
.authors { display: flex; flex-direction: column; gap: 14px; margin-top: 4px; }
.author-row { display: flex; gap: 12px; align-items: flex-start; }
.author-avatar { font-size: 32px; flex-shrink: 0; }
.author-row strong { font-size: 15px; font-weight: 800; display: block; }
.author-row p { color: var(--text-mid); font-size: 13px; margin-top: 2px; }
</style>
