'use strickt';

const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const mode = require('gulp-mode')();
const uglify = require('gulp-uglify');
const cssnano = require('cssnano');
const postcss = require("gulp-postcss");
const autoprefixer = require('autoprefixer');
const rename = require('gulp-rename');
const sourcemaps = require('gulp-sourcemaps');
const changed = require('gulp-changed');
const browserSync = require('browser-sync').create();
const webpack = require('webpack-stream');
const rimraf = require('rimraf');

// Path configuration
let paths = {
    styles: {
        src: "src/scss/**/*.scss",
        dest: "dist/assets/css/"
    },
    scripts: {
        src: "src/js/index.js",
        dest: "dist/assets/js/"
    },
    vendors: {
        src: "src/assets/js/vendors/**/*.*",
        dest: "dist/assets/js/vendors"
    },
    fonts: {
        src: "src/assets/fonts/**/*.*",
        dest: "dist/assets/fonts"
    },
    images: {
        src: "src/assets/img/**/*.*",
        dest: "dist/assets/img"
    }
};

// Server
gulp.task('server', function () {
    browserSync.init({
        server: {
            port: 9000,
            baseDir: "dist",
            injectChanges: true
        }
    });

    gulp.watch('dist/**/*').on('change', browserSync.reload);
});

// Styles compile
gulp.task('styles:compile', function () {
    return gulp.src(paths.styles.src)
        .pipe(mode.development(sourcemaps.init()))
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss([autoprefixer({
            overrideBrowserslist: [''], // ['last 2 versions'] or ['> 1%']
            cascade: false
        }), cssnano()]))
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(mode.development(sourcemaps.write('../maps')))
        .pipe(gulp.dest(paths.styles.dest));
});

// JavaScript compile
gulp.task('scripts:compile', function () {
    return gulp.src(paths.scripts.src)
        .pipe(webpack({
            mode: mode.development() ? 'development' : 'production',
            output: {
                filename: 'app.js'
            },
            module: {
                rules: [
                    {
                        test: /\.m?js$/,
                        exclude: /(node_modules)/,
                        use: {
                            loader: 'babel-loader',
                            options: {
                                presets: ['@babel/preset-env']
                            }
                        }
                    }
                ]
            },
            externals: {
                jquery: 'jQuery',
                bootstrap: 'bootstrap'
            },
        }))
        .pipe(mode.development(sourcemaps.init()))
        .pipe(mode.production(uglify().on('error', (uglify) => {
            console.error(uglify.message);
            this.emit('end');
        })))
        .pipe(rename({ suffix: '.min' }))
        .pipe(mode.development(sourcemaps.write()))
        .pipe(gulp.dest(paths.scripts.dest));
});

// Clean assets folder
gulp.task('clean', function del(cb) {
    return rimraf('dist/assets', cb);
});

// Copy fonts
gulp.task('copy:fonts', function () {
    return gulp.src(paths.fonts.src)
        .pipe(changed(paths.fonts.dest))
        .pipe(gulp.dest(paths.fonts.dest));
});

// Copy images
gulp.task('copy:images', function () {
    return gulp.src(paths.images.src)
        .pipe(changed(paths.images.dest))
        .pipe(gulp.dest(paths.images.dest));
});

// Copy JavaScript vendors
gulp.task('copy:vendors', function () {
    return gulp.src(paths.vendors.src)
        .pipe(changed(paths.vendors.dest))
        .pipe(gulp.dest(paths.vendors.dest));
});

// Copy assets
gulp.task('copy:assets', gulp.parallel('copy:fonts', 'copy:images', 'copy:vendors'));

// Watchers
gulp.task('watch', function () {
    gulp.watch('src/scss/**/*.scss', gulp.series('styles:compile'));
    gulp.watch('src/js/**/*.js', gulp.series('scripts:compile'));
    gulp.watch('src/assets/**/*.*', gulp.series('copy:assets'));
});

// Build task
gulp.task('build', gulp.parallel('styles:compile', 'scripts:compile', 'copy:assets'));

// Default task
gulp.task('default', gulp.series(
    gulp.parallel('styles:compile', 'scripts:compile', 'copy:assets'),
    gulp.parallel('watch', 'server')
));
