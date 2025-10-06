export default {
  content: ["./templates/**/*.html"],
  darkMode: ['selector', '[data-bs-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        border: '#e4e4e7',
        bgCard: '#ffffff',
        bgSoft: '#f8fafc',
        fgMuted: '#71717a',
        fg: '#18181b',
      },
      ringColor: ({ theme }) => ({
        DEFAULT: theme('colors.zinc.400'),
      }),
      boxShadow: {
        subtle: '0 1px 2px 0 rgb(0 0 0 / 0.04), 0 1px 1px -1px rgb(0 0 0 / 0.08)',
      },
      transitionTimingFunction: {
        smooth: 'cubic-bezier(.2,.8,.2,1)',
      }
    }
  }
}
