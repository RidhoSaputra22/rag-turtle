Project ini bertujuan meneksplore kemungkinan penggunaann model kecil untuk kebutuhan agentik dengan menggunakan JSON sebagai alat komunikasi otak (model) dan penggerak (Sistem)

Pada kasus ini penulis bertujuan untuk membuat sistem yang dapat mengambar pemandangan menggunakan model kecil seprti qween atai gemma menggunakan python library turtle sebagai perantaranya


Cara kerjanya adalah dengan membuat skill skill kecil yang compact yang lalu menyuruh model untuk mengenerate file JSON berisi struktur aksi - aksi yang akan di lakukan model

## Alur generasi scenery

Model sekarang bekerja dalam dua tahap agar hasil JSON dari model kecil lebih
konsisten dan scenery tidak tampak kosong:

1. Model membuat `SceneryPlan`: art direction, palet, layer, fokus, dan daftar
   objek dari belakang ke depan.
2. RAG mengambil recipe komposisi dan objek yang relevan.
3. Model mengubah plan menjadi `Scene` JSON. Kedua respons dipaksa mengikuti
   JSON Schema dari Pydantic melalui Ollama.
4. Sistem memvalidasi, menormalisasi warna/properti, menjaga urutan layer, dan
   melengkapi kembali objek plan yang hilang sebelum Turtle menggambar.

Untuk request pemandangan, guardrail komposisi menambahkan depth yang relevan
(misalnya meadow, hill, awan, semak, atau bunga) bila model kecil menghasilkan
plan yang valid tetapi terlalu kosong. Elemen yang tidak diminta tidak akan
dipakai untuk request bentuk tunggal seperti `circle`.

Contoh JSON scene yang dapat dirender:

```json
{
  "background": "skyblue",
  "objects": [
    {
      "type": "meadow",
      "position": "bottom",
      "size": "large",
      "color": "#78b957",
      "secondary_color": "#9fd278",
      "layer": "background",
      "properties": {"offset_y": -55, "width_scale": 1.05}
    },
    {
      "type": "tree",
      "position": "bottom-right",
      "size": "medium",
      "color": "forestgreen",
      "secondary_color": "#5fae5d",
      "layer": "foreground",
      "properties": {"offset_x": -45, "offset_y": 45}
    }
  ]
}
```

Setelah mengambil perubahan knowledge, bangun ulang index RAG:

```bash
python3 -m rag.index_knowledge
python3 main.py
```

