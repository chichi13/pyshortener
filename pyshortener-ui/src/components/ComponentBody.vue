<template>
  <div class="flex flex-grow items-center justify-center">
    <form class="w-5/6 lg:w-2/3 bg-white shadow-md rounded-lg px-8 py-8">
      <span
        class="block text-center text-gray-700 text-3xl font-semibold mb-2 pb-6"
        >Paste the URL to be shortened</span
      >
      <input
        class="w-full md:w-3/4 shadow border rounded py-2.5 px-3 mr-4 mb-4 lg:mb-0 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        type="text"
        placeholder="kactica.com"
      />
      <button
        class="w-full md:w-1/5 bg-blue-400 p-2.5 rounded text-white font-semibold hover:bg-blue-600"
      >
        Create Shortlink
      </button>
    </form>
  </div>
</template>
