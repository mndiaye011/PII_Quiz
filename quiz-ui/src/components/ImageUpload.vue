<template>
  <div class="upload-wrap">
    <label class="upload-label" :for="inputId">
      <span class="upload-icon">📎</span>
      <span>{{ fileName || 'Choisir une image' }}</span>
    </label>
    <input :id="inputId" type="file" accept="image/*" class="upload-input" @change="handleChange" />
    <button v-if="fileName" type="button" class="remove-btn" @click="removeFile">✕ Retirer</button>
  </div>
</template>

<script>
export default {
  emits: ['file-change'],
  data() {
    return { fileName: '', inputId: 'img-upload-' + Math.random().toString(36).slice(2) };
  },
  methods: {
    handleChange(e) {
      const file = e.target.files[0];
      if (!file) return;
      this.fileName = file.name;
      const reader = new FileReader();
      reader.onload = (ev) => this.$emit('file-change', ev.target.result);
      reader.readAsDataURL(file);
    },
    removeFile() {
      this.fileName = '';
      this.$emit('file-change', '');
    },
  },
};
</script>

<style scoped>
.upload-wrap { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.upload-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 16px;
  border: 1.5px dashed var(--border);
  border-radius: var(--radius);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-mid);
  cursor: pointer;
  transition: all 0.15s;
  background: var(--off-white);
}
.upload-label:hover { border-color: var(--navy); color: var(--navy); }
.upload-input { display: none; }
.remove-btn {
  background: none;
  border: 1.5px solid #fca5a5;
  color: #d63030;
  padding: 8px 14px;
  border-radius: var(--radius);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: var(--font);
  transition: all 0.15s;
}
.remove-btn:hover { background: #fef2f2; }
</style>
