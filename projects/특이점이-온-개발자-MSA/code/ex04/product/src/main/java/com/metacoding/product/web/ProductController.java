package com.metacoding.product.web;

import com.metacoding.product.usecase.*;
import org.springframework.http.ResponseEntity;
import com.metacoding.product.core.util.Resp;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductController {
    private final GetProductUseCase getProductUseCase;
    private final GetAllProductsUseCase getAllProductsUseCase;

    @GetMapping("/{productId}")
    public ResponseEntity<?> getProduct(@PathVariable("productId") int productId) {
        return Resp.ok(getProductUseCase.findById(productId));
    }

    @GetMapping
    public ResponseEntity<?> getAllProducts() {
        return Resp.ok(getAllProductsUseCase.findAll());
    }
}
